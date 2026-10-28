---
type: decision
title: delay-hpbc-submission-with-30-minute-cancellation-window
project: tomale-rn-v1
status: accepted
date: 2026-10-14
features:
  - F-store
  - F-print-fulfilment
---

# Decision: delay-hpbc-submission-with-30-minute-cancellation-window

## What we decided

Orders wait 30 minutes after payment (1 minute for test users) before being submitted to HPBC. Submission moves out of the `order_fulfilment_check` DB trigger into a new `hpbc_submit_due_orders` background task (every 60 s, up to 20 orders per run) gated on `store_orders.submit_after`, which the Stripe webhook sets on payment. Delay values live in the environment variables `hpbc_submit_delay_minutes` (30) and `hpbc_submit_delay_minutes_test` (1). `reconcile_order_fulfilment` checks the order is not Cancelled and `submit_after` has passed, and re-reads the order after setting the lock. `hpbc_create_order` also checks for Cancelled.

## Why

Pureprint's real trigger sequence shows Order Print Ready is batched and cannot be backed out, so the only safe cancellation point is before submission. A delay window lets customers cancel and be refunded automatically. Moving submission out of the trigger also resolves the "synchronous HPBC call inside a DB trigger" risk.

## Alternatives considered

Not discussed in session notes beyond the previous design, where the DB trigger submitted orders immediately.

## Trade-offs accepted

Fulfilment is delayed by 30 minutes for real orders. The task's history is set to 0, so task errors are currently invisible (to be turned on temporarily when diagnosing order 134, which was not submitted within the 4-minute test poll; root cause not yet found).

## Workflow detail

Built through the Xano AI from `spec_delayed_hpbc_submission_2026-10-14.md`. Postman 3C-2 is now a bounded poll (12 × 20 s). New cancel-window tests are still to be added. A newly created Xano task may be inactive, so check it is switched on.

## Related notes

- [[automate-full-refund-on-self-service-cancel]]
- [[disallow-cancelling-personalised-orders-once-in-production]]
- [[enforce-forward-only-hpbc-callback-status-transitions]]
- [[mark-order-error-on-hpbc-rejection-and-clear-lock]]
- [[replace-manual-test-gates-with-bounded-polling]]
- [[order-fulfilment-flow]]
- [[2026-10-14-001]]
