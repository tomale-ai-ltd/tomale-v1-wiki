---
type: decision
title: add-order-status-guard-to-stripe-checkout
project: tomale-rn-v1
status: accepted
date: 2026-10-23
related:
  - "[[2026-10-23-001]]"
  - "[[block-ordering-of-stories-awaiting-parental-approval]]"
affects:
  - "[[api-spec]]"
  - stripe/create_checkout_session
features:
  - F-store
  - F-payments
---

# Decision: add-order-status-guard-to-stripe-checkout

## What we decided

`stripe/create_checkout_session` returns 400 `ORDER_NOT_PAYABLE` unless the order is `Draft` or `Payment Pending`. Added alongside the parental-approval gate and recorded as an extension of [[api-spec]].

## Why

Not discussed in session notes.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Built 23/10 in the same change as the `STORY_AWAITING_APPROVAL` gate on checkout. Covered by the Phase 1 final `_tests` regression (86/86).

## Related notes

- [[2026-10-23-001]]
- [[block-ordering-of-stories-awaiting-parental-approval]]
- [[verify-stripe-checkout-totals-against-xano-prices]]
- [[order-fulfilment-flow]]
- [[6-api-security-model]]
