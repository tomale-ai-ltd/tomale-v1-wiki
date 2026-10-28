---
type: decision
title: omit-preflight-timescales-and-unit-prices-from-hpbc-orders
project: tomale-rn-v1
status: accepted
date: 2026-10-13
features:
  - F-print-fulfilment
---

# Decision: omit-preflight-timescales-and-unit-prices-from-hpbc-orders

## What we decided

We do not send preflight profile, production timescales, `unitPrice` or `unitCost` in HPBC (Pureprint) order payloads. These are configured per SKU on Pureprint's side. The shipping alias is sent from `store_orders.shipping` (`standard` = Royal Mail 48 Tracked, `express` = Royal Mail 24 Tracked).

## Why

Pureprint's reply: preflight (PDF/X-1a or PDF/X-4) is set on their side; timescales (softback 2 / hardback 3 working days, 5pm cutoff) are SKU config; `unitPrice`/`unitCost` should be left empty (1/1 are SKU defaults, customs value only needed for international).

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes. PDF requirements (PDF/X-4, bleed/trim, orientation) still await Alex's confirmation.

## Workflow detail

Keep PDF URLs live for at least 2 hours after submission. No payload changes needed for these fields.

## Related notes

- [[make-hpbc-create-order-a-single-fail-closed-request]]
- [[scope-hpbc-callbacks-to-six-customer-facing-statuses]]
- [[order-fulfilment-flow]]
- [[2026-10-13-001]]
