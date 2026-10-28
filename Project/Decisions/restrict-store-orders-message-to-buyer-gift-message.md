---
type: decision
title: restrict-store-orders-message-to-buyer-gift-message
project: tomale-rn-v1
status: accepted
date: 2026-10-15
features:
  - F-store
---

# Decision: restrict-store-orders-message-to-buyer-gift-message

## What we decided

`store_orders.message` holds the buyer's gift message only. Callback text from HPBC/Pureprint goes to `store order updates`, not to `store_orders.message`.

## Why

`hpbc_update_order` had an input named `message`, which overwrote the buyer's gift message with Pureprint text on every HPBC callback.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

The `hpbc_update_order` input is now `update_message`, and both HPBC status callback endpoints map the incoming `message` to it.

## Related notes

- [[2026-10-15-001]]
- [[order-fulfilment-flow]]
- [[enforce-forward-only-hpbc-callback-status-transitions]]
- [[avoid-column-named-function-inputs-in-xano]]
