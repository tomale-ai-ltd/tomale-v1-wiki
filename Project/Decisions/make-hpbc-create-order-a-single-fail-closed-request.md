---
type: decision
title: make-hpbc-create-order-a-single-fail-closed-request
project: tomale-rn-v1
status: accepted
date: 2026-10-13
features:
  - F-print-fulfilment
---

# Decision: make-hpbc-create-order-a-single-fail-closed-request

## What we decided

`print on demand/hpbc_create_order` is rebuilt as one request that serves staging and live. The SKU fails closed to staging unless `users.test_mode` is explicitly false. Preconditions: order exists, not already submitted (`hpbc_order_id` empty), SKU present, shipping alias `standard` or `express`, and both PDF URLs present. The unused instant stories lookup was removed.

## Why

Fail-closed SKU selection prevents a test user from accidentally creating a live (printed and charged) order. The `hpbc_order_id` check prevents resubmitting an order. Confirmed that `test_mode` is reachable inside the function.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

The failure path is silent: on HPBC rejection the lock clears but the order is not marked Error. Marking Error is the next-session item.

## Workflow detail

Live SKUs `TOM-001` / `TOM-002` are stored in `products.hpbc_sku_live`. One end-to-end live test per SKU is needed before accepting customer orders.

## Related notes

- [[order-fulfilment-flow]]
- [[key-hpbc-environment-switch-off-stripe-test-mode]]
- [[run-real-fulfilment-cascade-against-staging-sku]]
- [[2026-10-13-001]]
