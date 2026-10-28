---
type: decision
title: store-hpbc-tracking-on-store-orders
project: tomale-rn-v1
status: accepted
date: 2026-10-13
features:
  - F-store
  - F-print-fulfilment
---

# Decision: store-hpbc-tracking-on-store-orders

## What we decided

Tracking data from the HPBC Shipped callback is stored on `store_orders` in new `tracking_url` and `tracking_number` fields. They are mapped as optional inputs on `hpbc/webhook_statusCallbackUrl` (#217) → `hpbc_update_order` using `first_notempty`, so later callbacks never clear them. Pureprint's Shipped template was updated to include the fields.

## Why

Tracking is needed on the order once shipped; `first_notempty` stops later callbacks (e.g. Error) wiping it.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Callback status transition rules are not yet decided; the handler currently lets Error overwrite Shipped.

## Workflow detail

`GET /store_orders/{id}` now returns the tracking fields, `hpbc_order_id`, `cover_pdf` and `inner_pdf`. Postman 3D-2 asserts tracking after Shipped and 3D-3 asserts it is kept after Error.

## Related notes

- [[scope-hpbc-callbacks-to-six-customer-facing-statuses]]
- [[replace-manual-test-gates-with-bounded-polling]]
- [[order-fulfilment-flow]]
- [[2026-10-13-001]]
