---
type: decision
title: store-money-as-integer-minor-units
project: tomale-rn-v1
status: accepted
date: 2026-07-15
---

---

# Decision: store-money-as-integer-minor-units

## What we decided

Money is stored as an integer, `amount_minor`, paired with `currency`, replacing the old float `price` field on `transactions`. This matches Stripe's native representation (`amount_total` from `data.object`) directly.

## Why

Float types cannot represent many money values exactly, and that error accumulates across refund arithmetic. Storing what Stripe sends — an integer — paired with its currency, and dividing only for display, avoids float rounding errors. The `currency` pairing matters because not all currencies use 100 minor units, so a hardcoded divide-by-100 on display would be wrong for some currencies.

## Alternatives considered

The float `price` field this replaces.

## Trade-offs accepted

Not discussed in session notes beyond the float-precision rationale.

## Workflow detail

Applies to the `transactions` table restructure; the unique index on `provider_payment_id` was confirmed to reject duplicate inserts as part of the same rebuild. Any future display logic must divide by the currency's actual minor-unit factor rather than assuming 100.

## Related notes

[[Sessions/2026-07-15-001]]
[[record-transactions-drop-checkout-session-object]] — same restructure
[[split-refund-model-into-self-service-and-support-paths]] — same table, refund arithmetic is the reason float precision matters
