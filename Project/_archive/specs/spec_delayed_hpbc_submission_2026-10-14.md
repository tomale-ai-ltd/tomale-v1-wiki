# Delayed HPBC submission, 30-minute cancellation window, and self-service refunds

## Goal
Paid print orders must not be sent to HPBC (Pureprint) immediately. Each order waits 30 minutes after payment confirmation. During that window the customer can cancel and is refunded automatically. After the window, a background task submits the order. Submission moves out of the store_orders database trigger.

## 1. Schema
Add two nullable timestamp fields to the `store orders` table: `submit_after` and `cancelled_at`. Neither field gets a default value. Do not change any other field, including `created_at`.

Add two fields to the `transactions` table, used on the original payment row to track refund attempts: `refund_attempt_count` (int, default 0) and `refund_last_attempt_at` (nullable timestamp, no default).

## 2. Environment variables
Add `hpbc_submit_delay_minutes` with the value 30, and `hpbc_submit_delay_minutes_test` with the value 1. Store both as text and cast them to integers wherever they are used.

## 3. Set submit_after on payment
In `stripe_webhook_payment_confirmation`, at the step where the order is marked paid, also set `submit_after`. Use the `users.test_mode` value of the order's owner (`store_orders.users_id`):
- If `test_mode` is explicitly true, set `submit_after` to now plus `hpbc_submit_delay_minutes_test`.
- In every other case, including null, set it to now plus `hpbc_submit_delay_minutes`.

Set `submit_after` only if it is currently empty, so a replayed webhook never pushes it back. Do not use `$auth` anywhere, because the webhook has no auth context.

## 4. Stop trigger-driven submission
Disable the `order_fulfilment_check` table trigger, or remove its call to `docgen/reconcile_order_fulfilment`. PDFs still generate and attach as they do today. Only submission timing changes. Leave the `audit_store_orders_changes` trigger in place.

## 5. New background task: submit due orders
Create a scheduled task named `hpbc_submit_due_orders` that runs every 2 minutes. It queries `store orders` for records where all of the following are true:
- `payment_status` is "Confirmed"
- `status` is not "Cancelled" and not "Error"
- `cover_pdf` and `inner_pdf` are both present
- `hpbc_order_id` is empty
- `hpbc_lock` is false
- `submit_after` is present and less than or equal to now

Sort the results by `submit_after` ascending and limit them to 20 per run. For each order, call `docgen/reconcile_order_fulfilment` with its id inside a try/catch, so one failing order does not stop the others. Log failures. Set the task's request history to off or a small limit. It must never use `$auth`.

## 6. Tighten reconcile_order_fulfilment
Extend its precondition so it also requires:
- `status` is not "Cancelled"
- `submit_after` is present and less than or equal to now

After it sets `hpbc_lock` to true, it must re-read the order. If the status is now "Cancelled", it sets `hpbc_lock` back to false and stops without calling `hpbc_create_order`. Set its request history to off.

## 7. Last-moment check in hpbc_create_order
Add a precondition after the order is fetched: `status` must not be "Cancelled". If the precondition fails, clear `hpbc_lock` before throwing. Also clear `hpbc_lock` on every other precondition failure, and if the HPBC request itself throws (timeout or network failure). A failed submission must never leave the order locked. On a non-2xx response from HPBC, set the order `status` to "Error" (already drafted). Set request history to off, because the request carries the HPBC auth header.

## 8. New endpoint: customer cancel
Add `POST /store_orders/{store_orders_id}/cancel` in the `app` API group, authenticated against `users`.
- Look the order up by id with `users_id == $auth.id`. If none is found, return 404 `ORDER_NOT_FOUND`.
- If any of the following conditions is false, return 422 `ORDER_NOT_CANCELLABLE` with the message "This order has gone to print and can no longer be cancelled.":
  - `payment_status` is "Confirmed"
  - `status` is not already "Cancelled"
  - `hpbc_order_id` is empty
  - `hpbc_lock` is false

  Do not add a check on `submit_after`. Once the window has passed, cancellation is only possible until the background task claims the order.
- If all checks pass:
  1. Set `status` to "Cancelled", `cancelled_at` to now, and `last_modified_at` to now.
  2. Add a `store order updates` row with the message "Cancelled by customer".
  3. Call the refund function from section 8a. If the refund call fails, do not undo the cancellation, because the order must still never print. Return 200 with `refund_status: "pending"`, and let the retry task in section 8b finish the refund.
- Optionally, mark any of the order's queued `pdf_jobs` as cancelled, to avoid paying Papermill for unused PDFs.
- Return the order id and status.

## 8a. New function: payments/stripe_refund_order
This implements the self-service refund path from decision split-refund-model-into-self-service-and-support-paths, using the existing `transactions` table.

Input: `store_orders_id`.

1. Load the order. It must be "Cancelled" with an empty `hpbc_order_id`; otherwise fail. Refunds through this path are only allowed before HPBC submission.
2. Find the order's original Stripe payment row in `transactions` (`store_orders_id` matches, provider "stripe", type payment). It must exist and have `refundable_amount` greater than 0. If `refundable_amount` is already 0, return success without calling Stripe, so the function is safe to run twice.
3. Test shortcut: follow the existing `pdf_force_success` pattern. If env `refund_force_success` is "true" and the order owner's `users.test_mode` is true, skip Stripe and treat the refund as succeeded, with a fake id `re_test_{store_orders_id}`. This is needed because the Postman `_tests` payment is a simulated webhook, so its payment intent does not exist in Stripe and a real refund call would fail.
4. Otherwise, call the Stripe API with POST `https://api.stripe.com/v1/refunds`, form-encoded:
   - `payment_intent` = the transaction's `provider_payment_id`
   - `amount` = `refundable_amount`
   - `reason` = `requested_by_customer`
   - `metadata[store_orders_id]` = the order id

   Send the header `Idempotency-Key: refund_{store_orders_id}_{refund_attempt_count}`, using `refund_attempt_count` from the payment row. Stripe stores the result of a key for 24 hours, so reusing the same key after a confirmed failure would only return the same failure. The count therefore increases only after a confirmed failure (section 8c). A network retry reuses the same key, which is what stops a double refund. Use the same Stripe secret key environment variable that the checkout functions use. Do not add a mode flag, because test or live is decided by the key.
5. On success, when the Stripe refund status is "succeeded" or "pending":
   - Add a `transactions` row: provider "stripe", type "refund", `provider_payment_id` = the refund id (`re_...`), the same `users_id` and `store_orders_id`, `amount_minor` = the refunded amount, `currency` from the original row, and `status` from Stripe.
   - Set the original payment row's `refundable_amount` to 0.
   - Add a `store order updates` row with the message "Refund issued".
6. On failure (the Stripe request errors, or the refund comes back with status "failed"), increase `refund_attempt_count` by 1 and set `refund_last_attempt_at` to now on the payment row. Leave `refundable_amount` unchanged so the retry task picks the order up. If Stripe returns a refund object with status "failed", also add the `transactions` refund row with status "failed", as a record.
7. Response: `{ok, refund_status, refund_id}`. Set request history to off, because the request carries the Stripe secret key.

## 8b. New background task: retry pending refunds
Create a scheduled task named `reconcile_order_refunds` that runs every 15 minutes. It finds orders whose `status` is "Cancelled", whose `hpbc_order_id` is empty, and whose Stripe payment transaction still has `refundable_amount` greater than 0. For each one it calls `payments/stripe_refund_order` inside a try/catch. The idempotency key makes retries safe. Mirror the `reconcile_stripe_customers` pattern. Skip a payment row when `refund_attempt_count` is 5 or more, and leave at least 15 minutes after `refund_last_attempt_at` before retrying. When an order reaches 5 attempts, add a `store order updates` row with the message "Refund failed after 5 attempts: manual handling" so support can see it.

## 8c. Handle Stripe refund status webhooks
A card refund can come back from Stripe as "pending" and fail later. This handling picks that up.

Stripe dashboard: add `refund.updated` and `refund.failed` to the event subscriptions of the existing webhook endpoint (`POST /stripe/webhook_payment_confirmation` in the `webhooks` API group). Use the same signing secret; there is no new endpoint. If the account's API version does not emit `refund.failed`, `refund.updated` alone is enough, because it carries the status change.

In `stripe/webhook_payment_confirmation`, keep the existing flow unchanged: signature verification, `webhook_event_ingest` into `transaction_webhook_events` (dedup on `dedup_key`), duplicate short-circuit, and `webhook_event_complete` at the end. Add a branch for `event_type` values `refund.updated` and `refund.failed`, before the current store-and-acknowledge step for unknown types. In that branch, `data.object` is a Stripe refund object:

1. Read `data.object.id` (refund id), `data.object.status`, `data.object.amount`, `data.object.payment_intent`, `data.object.failure_reason` and `data.object.metadata.store_orders_id`.
2. Look up the `transactions` row where `provider` is "stripe", `type` is "refund" and `provider_payment_id` equals the refund id.
3. If the row is found:
   - Set its `status` to `data.object.status`.
   - If the new status is "failed" or "canceled" and the previous status was not, find the original payment row (same `store_orders_id`, type payment) and do three things: add `data.object.amount` back to its `refundable_amount`, increase its `refund_attempt_count` by 1, and set `refund_last_attempt_at` to now. Then add a `store order updates` row with the message "Refund failed: {failure_reason}. Retrying.". The `reconcile_order_refunds` task will retry it with a new idempotency key.
   - If the new status is "succeeded", nothing else changes.
4. If no row is found, the refund was most likely made by hand in the Stripe dashboard, which is the support-driven path. Find the payment row by `provider_payment_id` = `data.object.payment_intent` and add a `transactions` refund row with the refund id, amount and status. Do not change `refundable_amount`, because that field belongs to the self-service path only. Add a `store order updates` row with the message "Refund made outside the app: review". If no payment row is found either, store the event and acknowledge it.
5. Always return 200 once the event is stored, including in the no-match case. Record processing errors through `webhook_event_complete` (`processing_errors`), in line with the existing differentiate-ingest-vs-processing-failure decision.
6. Do not use `$auth`.

## 9. Expose cancellability to the app
In `GET /store_orders/{store_orders_id}`, add `submit_after` to the output and a computed boolean `cancellable`. `cancellable` is true when the order is paid, not Cancelled, not locked and has no `hpbc_order_id`.

## 10. Accepted residual risk
There is a very small race. A customer cancel can land in the milliseconds between reconcile setting the lock and `hpbc_create_order` sending the request. If that happens, the order is printed and also refunded. The re-reads in steps 6 and 7 make this window as small as practical. Do not add further locking.

## 11. Tests to add in Postman (_tests)
- Increase C1's poll window so it covers the 1-minute test delay plus one task interval (roughly 3–4 extra minutes).
- Add a cancel-in-window test. Pay for a new test order, immediately call the cancel endpoint, and assert all of the following:
  - the response is 200 with status "Cancelled"
  - after waiting past the window plus one task interval, `hpbc_order_id` is still empty
  - a `transactions` row with type refund exists (the fake `re_test_` id via `refund_force_success`)
  - the payment row's `refundable_amount` is 0
  - calling cancel again returns 422 and no second refund row appears
- Add a refund-failure test. Send a signed, simulated `refund.updated` event, built the same way as the simulated `checkout.session.completed`. Use `data.object.id` = the test refund id `re_test_{orderId}`, status "failed", and the refunded amount. Assert three things: the refund row's `status` is "failed", the payment row's `refundable_amount` is back to the full amount, and `refund_attempt_count` has increased by 1.
- Send the same event again and assert it is caught as a duplicate (`transaction_webhook_events` dedup), with no second change to `refundable_amount`.
- Add a negative test. Try to cancel an order that already has an `hpbc_order_id` and expect 422 `ORDER_NOT_CANCELLABLE`. Calling cancel with another user's token returns 404.
- Do one manual check outside `_tests`. Pay with a real Stripe test card (4242 4242 4242 4242) through the checkout URL, cancel within the window, and confirm that the refund appears in the Stripe test dashboard. This is the only check that exercises the real Stripe refund call.

## 12. Environment variables (summary)
- `hpbc_submit_delay_minutes` = 30
- `hpbc_submit_delay_minutes_test` = 1
- `refund_force_success` = "true" in this workspace while testing; set it to "false" (or remove it) in prod.
