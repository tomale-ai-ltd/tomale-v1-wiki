---
type: prd
title: PRD-Order-PoD-System
project: tomale-rn-v1
status: current
version: 2.0
date: 2026-04-14
last_verified: 2026-10-29
owner: vault
features:
  - F-print-fulfilment
  - F-store
related:
  - "[[PRD-Store-Orders]]"
  - "[[order-fulfilment-flow]]"
  - "[[backend-xano]]"
---

# **MICRO-PRD: Order & Print-on-Demand System**

> **Changes in 2.0 (B9, 29/10/2026):** the original principle "images only after payment" is replaced: stories and illustrations are created in the app first, and **entitlements limit generation** ([[gate-image-generation-with-entitlements-at-story-creation]]). This PRD now covers the print side as built: Papermill PDFs, HPBC/Pureprint, the live `store_orders` state machine, the 30-minute cancel window, refunds. The old `orders` / `order_assets` / `payments` tables were never built; the live tables are `store_orders`, `pdf_jobs` and `transactions`.

## **Goal**
Let users order a printed copy of a story they've already made, safely: no irreversible print cost before payment, no surprise charges, and a clear record for every printed book.

## **Scope**
Covers:
- Paid order → print-ready PDFs → submission to the printer → status callbacks
- Cancellation and refunds
- Test vs live printing

## **Non-Goals**
- Image generation (happens at story creation, [[PRD-Chatbot-Story-Conversations]]). A story's images can't be regenerated after creation in V1 ([[v2-backlog]])
- Bulk orders
- Returns logistics
- Customer support tooling (later)

## **Core Principle**
**No irreversible print cost before payment, and none during the cancel window.** Submission to the printer happens only after payment is confirmed and the 30-minute window has passed.

## **Backend Requirements (built)**

### Data models
- **`store_orders`**: status, payment status, totals in pence, `submit_after`, `cancelled_at`, `cover_pdf`, `inner_pdf`, `hpbc_order_id`, `hpbc_lock`, tracking.
- **`pdf_jobs`**: cover and inner PDF jobs (Papermill), drained by `pdf_worker_tick`.
- **`transactions`**: payment and refund rows (`amount_minor`, `currency`, `provider_payment_id` unique, `refundable_amount`).
- **`transaction_webhook_events`**: every Stripe and HPBC event, stored before processing.

### Order state machine (live)
```
Draft → Payment Pending → Payment Confirmed → Order Confirmed → In Production → Shipped
                                    ↘ Cancelled (within the window, auto refund)
Any pre-Shipped state → Error (printer rejection, PDF failure, timeout) → manual check
```
- Statuses only move forward; `Error` can be recovered by a later forward status; `Cancelled` only before In Production ([[enforce-forward-only-hpbc-callback-status-transitions]]).
- Submission: `hpbc_submit_due_orders` (every 60 s, up to 20) picks orders that are paid, have both PDFs, aren't locked or submitted, and are past `submit_after` ([[delay-hpbc-submission-with-30-minute-cancellation-window]]).
- `hpbc_create_order` is one fail-closed request; any failure marks the order `Error` and releases the lock ([[make-hpbc-create-order-a-single-fail-closed-request]]).
- Test vs live: the user's `test_mode` picks the test or live SKU and Stripe keys, failing closed to test ([[key-hpbc-environment-switch-off-stripe-test-mode]]). **Pre-launch:** new sign-ups must get `test_mode = false`.

### Refund policy (live)
- **Self-service cancel** inside the window, before submission: automatic full Stripe refund ([[automate-full-refund-on-self-service-cancel]]).
- **After submission:** no cancellation; personalised goods are exempt from the 14-day right (Consumer Contracts Regulations 2013, reg. 28(1)(b)) ([[disallow-cancelling-personalised-orders-once-in-production]]).
- **Misprints and quality issues:** support-driven, discretionary ([[split-refund-model-into-self-service-and-support-paths]]).

## **Backend prep** (from the generated [[Repos/tomale-rn-test/memory/data-model|data-model]] and the live code)
**Live:** the whole chain above, tested end to end against the test SKU (Postman `_tests` folders 3 and 4).

**To build:**
1. **Hardback:** a second product with its own HPBC SKUs (test and live) and Papermill templates (a hardback cover has a different layout from a paperback); check the PDF jobs pick the template from the product.
2. **Gift message page:** confirm the inner PDF template prints `store_orders.message` on the first page, and leaves it blank when there's no message.
3. ~~£0 orders~~ (Club's monthly book): V2 with Club ([[v2-backlog]]).
4. **Live printing:** live SKUs, live callback URLs and token, and new sign-ups with `test_mode = false` ([[pre-launch-checklist]]).
5. **Timeouts:** ask Pureprint whether a repeated `sourceOrderId` is rejected; if so, timeouts can retry instead of going to `Error`.
6. **Postman `_tests`:** a hardback order through to Order Confirmed.

## **Frontend Requirements**
### Order UX
1. Finished story → "Order a printed book"
2. Product (A4 landscape paperback or hardback) and shipping, with clear pricing
3. E-reader preview (cover, gift message on the first page, story pages) and the personalised-goods notice
4. Payment (Stripe Checkout in an in-app sheet)
5. Confirmation, then status updates in order history

### Mandatory copy (UX)
"This book is made just for your child. You can cancel within 30 minutes of paying; once printing starts, orders can't be cancelled."

### Failure states
- Payment fails → order stays unpaid; retry.
- PDF or printer failure → order `Error`; support contacts the customer.
- User cancels in time → Cancelled + Refunded.

## **Acceptance Criteria** (covered by Postman `_tests` folders 3 and 4)
- No order reaches the printer without confirmed payment and both PDFs.
- No order is submitted before `submit_after`.
- Cancel inside the window refunds in full and never reaches the printer.
- Cancel after submission is refused (`ORDER_NOT_CANCELLABLE`).
- Every printed book has a traceable order, payment and printer reference.

## **Open Questions**
- Hardback pricing and print specification (from Pureprint).
- Does Pureprint reject a repeated `sourceOrderId`? If so, timeouts could retry automatically instead of going to `Error`.

Resolved 29/10 (approved by Kyle): no story image regeneration in V1; it waits for the cheaper image pipeline ([[v2-backlog]]).
