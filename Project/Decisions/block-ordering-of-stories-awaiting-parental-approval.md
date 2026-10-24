---
type: decision
title: "block-ordering-of-stories-awaiting-parental-approval"
date: 2026-10-22
status: current
project: tomale-rn-v1
---

---

# Decision: block-ordering-of-stories-awaiting-parental-approval

## What we decided

Ordering is blocked for stories awaiting parental approval: if `parental_approval_required && !parent_approved`, `POST store_orders` and `stripe/create_checkout_session` return 400 `STORY_AWAITING_APPROVAL`. A negative Postman test covers it.

## Why

Not discussed in session notes beyond the gate being a Phase 1 task, enforced server-side on both order creation and checkout.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes. The gate was agreed 22/10 and built 23/10.

## Workflow detail

Adds a NEG Postman test to the `_tests` run. Order creation and checkout both need the check, so neither path can bypass it.

## Related notes

[[parental-gate-on-profile-switch]]
[[formalise-story-status-lifecycle]]
[[migrate-store-orders-money-fields-to-integer-pence]]
[[order-fulfilment-flow]]
