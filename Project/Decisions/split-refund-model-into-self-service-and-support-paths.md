---
type: decision
title: split-refund-model-into-self-service-and-support-paths
project: tomale-rn-v1
status: accepted
date: 2026-07-15
features:
  - F-store
  - F-payments
---

# Decision: split-refund-model-into-self-service-and-support-paths

## What we decided

The refund model is split into two separate paths. Self-service cancel before production is a state-gated, automated full refund, gated on the order being pre-HPBC-submission, and `refundable_amount` on the `transactions` table serves this path only. Misprint and quality refunds are support-driven and discretionary, likely resolved via an account credit — a separate future ledger that does not touch `refundable_amount`.

## Why

Not explicitly discussed beyond the state-gating rationale: a full automated refund is only safe while the order hasn't been submitted to HPBC for production, so that gate is what makes the self-service path automatable at all. Support-driven refunds (misprint, quality issues) are discretionary judgment calls that don't fit an automated state gate, so they're routed to a separate mechanism instead of overloading `refundable_amount`.

## Alternatives considered

Not explicitly discussed in session notes; the implicit alternative is a single refund mechanism covering both automated pre-production cancellation and discretionary support cases.

## Trade-offs accepted

The account-credit ledger for support-driven refunds is a separate future table, not yet built — recorded as a future direction item, not committed this session.

## Workflow detail

`refundable_amount` on `transactions` (seeded to the full amount on transaction creation) is scoped exclusively to the self-service, pre-HPBC-submission cancel path. The support-driven account-credit path is parked as a future item and does not yet have a workflow.

## Related notes

[[Sessions/2026-07-15-001]]
[[record-transactions-drop-checkout-session-object]] — same restructure, refund sequencing deferred from this decision
[[store-money-as-integer-minor-units]] — same table, money representation
