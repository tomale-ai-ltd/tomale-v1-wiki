---
type: decision
title: migrate-store-orders-money-fields-to-integer-pence
project: tomale-rn-v1
status: accepted
date: 2026-10-22
---

---

# Decision: migrate-store-orders-money-fields-to-integer-pence

## What we decided

`store_orders.subtotal` and `shipping_amount` move from decimal pounds to integer pence. Existing rows are migrated in place (`round(x * 100)`, nulls skipped) and the columns become `int`. The `store_orders/{id}` PATCH takes `products.amount` / `shipping_options.amount` directly, and `stripe/create_checkout_session` guards on `subtotal + shipping_amount`. HPBC still receives pounds: `hpbc_create_order` sets `orderData.amount = subtotal / 100.0`.

## Why

`products`, `shipping_options` and `transactions` were already integer pence; `store_orders` was the outlier. Aligning it removes pound/pence conversion between tables and applies the existing minor-units rule.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

The HPBC boundary needs an explicit divide-by-100, since it still expects pounds. The change was built and published but not tested on 22/10; it awaits the full `_tests` run.

## Workflow detail

Writer: `store_orders/{id}` PATCH. Readers: `stripe/create_checkout_session`, `hpbc_create_order`. Verification: stored values 2499 / 399, HPBC `amount: 24.99`, `created_at` unchanged. The refund metadata key (`metadata[store_orders_id]`) was already correct, so no change there.

## Related notes

[[store-money-as-integer-minor-units]]
[[verify-stripe-checkout-totals-against-xano-prices]]
[[order-fulfilment-flow]]
[[block-ordering-of-stories-awaiting-parental-approval]]
