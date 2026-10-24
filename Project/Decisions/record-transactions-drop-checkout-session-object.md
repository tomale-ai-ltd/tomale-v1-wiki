---
type: decision
title: record-transactions-drop-checkout-session-object
date: 2026-07-15
status: current
project: tomale-rn-v1
---

---

# Decision: record-transactions-drop-checkout-session-object

## What we decided

Payment facts are recorded as structured rows in a rebuilt `transactions` table (the money domain), not stored as a raw `checkout_session_object` on `store_orders`. The `transactions` table was restructured with `provider`, `type`, `provider_payment_id` (unique index), `users_id`, `store_orders_id`, `amount_minor`, `currency`, a populated `status` enum, and `refundable_amount`, replacing the old float `price` field. A transaction write (`db.add transactions`) was wired into the Stripe webhook endpoint, firing after the store order update and before the PDF orchestrator, reading `payment_intent`, `amount_total`, and `currency` from `data.object`, with `refundable_amount` seeded to the full amount. `store_orders.checkout_session_object` is confirmed dead — a grep of all store order endpoints, `reconcile_order_fulfilment`, `hpbc_create_order`, `hpbc_update_order`, the PDF orchestrator, and the frontend found nothing reads it; only the text `checkout_session_id` is used — and it is scheduled for removal in the cleanup sweep.

## Why

Payment facts belong in the money domain (`transactions`), not bolted onto the fulfilment record. This finishes the 2026-07-03 decision that Stripe normalises to a `transactions` row (see [[Sessions/2026-07-03-001]]). Keeping the raw Stripe object on `store_orders` mixed payment state into a table whose job is order fulfilment, and nothing in the codebase actually read that raw object — only the id.

## Alternatives considered

Continuing to carry the raw `checkout_session_object` on `store_orders` as the source of payment truth, rather than normalising into a dedicated table.

## Trade-offs accepted

Sequencing was deliberately narrowed: the schema restructure and the money write are in scope now, while refund and cancel flow are deferred to later work (see [[split-refund-model-into-self-service-and-support-paths]]). The Stripe transaction write is unit-verified but the full payment-to-fulfilment end-to-end path (payment → transaction → fulfilment trigger → HPBC create → callbacks) was not yet exercised as of this session, per the "Blockers / questions" note in the session log.

## Workflow detail

The transaction write sits between the store order update and the PDF orchestrator in the Stripe endpoint. `checkout_session_object` removal is carried into the Phase 1 cleanup sweep. `data-model.md` needs updating to reflect the `transactions` restructure and the dropped column (carried into the documentation refresh in "Next session").

## Related notes

[[Sessions/2026-07-15-001]]
[[Sessions/2026-07-03-001]] — originating decision that Stripe normalises to a `transactions` row
[[store-money-as-integer-minor-units]] — same restructure, money representation
[[split-refund-model-into-self-service-and-support-paths]] — same restructure, refund sequencing
