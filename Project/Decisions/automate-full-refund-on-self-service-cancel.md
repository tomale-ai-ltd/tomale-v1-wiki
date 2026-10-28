---
type: decision
title: automate-full-refund-on-self-service-cancel
project: tomale-rn-v1
status: accepted
date: 2026-10-14
features:
  - F-store
  - F-payments
---

# Decision: automate-full-refund-on-self-service-cancel

## What we decided

A self-service cancel within the window triggers an automatic full Stripe refund, implemented under [[split-refund-model-into-self-service-and-support-paths]]. `payments/stripe_refund_order` uses the idempotency key `refund_{order}_{refund_attempt_count}` and has a test shortcut (`refund_force_success`, which must be false in prod). A `reconcile_order_refunds` task retries every 15 minutes, up to 5 attempts. The Stripe webhook handles `refund.updated` and `refund.failed` (sandbox and live destinations subscribed). Refunds made by hand in the Stripe dashboard are recorded but never touch `refundable_amount`. `transactions` gains `refund_attempt_count`, `refund_last_attempt_at` and a `"refund"` type.

## Why

Stripe idempotency keys cache results for 24 h, so a retry after a confirmed failure needs a new key; keying on the attempt count gives safe retries without duplicate refunds.

## Alternatives considered

Not discussed in session notes beyond the existing self-service vs support split.

## Trade-offs accepted

`store_orders.payment_status` is not yet set to Refunded on success (to be added). Customer notifications for cancellations and refunds are deferred, as is the support refund / account-credit ledger.

## Workflow detail

Postman tests still to add: cancel in window, negative cancels (already submitted gives 422; another user gives 404), and a failed `refund.updated` that restores the refundable amount and is caught as a duplicate on resend. One manual test-card cancel and refund to be checked in the Stripe dashboard.

## Related notes

- [[split-refund-model-into-self-service-and-support-paths]]
- [[delay-hpbc-submission-with-30-minute-cancellation-window]]
- [[record-transactions-drop-checkout-session-object]]
- [[2026-10-14-001]]
