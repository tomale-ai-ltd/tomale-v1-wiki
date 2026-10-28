---
type: decision
title: make-store-orders-sku-based-and-draft-only-editable
project: tomale-rn-v1
status: accepted
date: 2026-07-03
related:
  - "[[2026-07-03-001]]"
  - "[[v1-audit]]"
affects:
  - products
  - store_orders PATCH
features:
  - F-store
---

# Decision: make-store-orders-sku-based-and-draft-only-editable

## What we decided

- Products are SKU-level: size and orientation are columns on `products`, one row per SKU. Revisit with a variants table only beyond about 20 SKUs.
- `store_orders` PATCH works only on `Draft` orders. Once payment starts, the order is immutable to the user, and changes go through support.
- Totals, currency and locale are always derived on the server, never accepted as input.

## Related notes

- [[2026-07-03-001]] (backfilled in B7)
- [[verify-stripe-checkout-totals-against-xano-prices]]
