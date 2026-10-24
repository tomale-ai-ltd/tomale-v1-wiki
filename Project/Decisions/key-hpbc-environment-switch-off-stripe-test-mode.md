---
type: decision
title: key-hpbc-environment-switch-off-stripe-test-mode
date: 2026-10-08
status: current
project: tomale-rn-v1
---

---

# Decision: Key the HPBC/Pureprint Environment Switch off the Stripe `test_mode` Flag

## What we decided

Select the staging vs. live print SKU from the same per-user `test_mode` flag that already drives Stripe test/live behaviour. `products` carries a staging SKU and a live SKU (`hpbc_sku_staging` / `hpbc_sku_live`; the code currently names them `hpbc_sku_test` / `hpbc_sku_live` and needs reconciling). The chosen SKU is injected into `print_specification.sku` at call time in `hpbc_create_order`, and the selection fails closed to staging.

## Why

Driving both Stripe and HPBC from one flag makes the dangerous mismatched states unreachable: a test payment with a live print order, or a live payment with a staging print order. The `_staging` SKUs route to the live Brand Centre but are rejected before production, so they exercise print-file preflight without real print cost.

## Alternatives considered

Not discussed in session notes beyond the separate per-environment approach (dev/prod separation, CTO Phase 2), which does not exist yet.

## Trade-offs accepted

This is an interim measure. It overlaps CTO Phase 2 (dev/prod separation, tasks 10–11) and should be retired in favour of environment-driven SKU selection once real environments exist. The SKU field names in code also need reconciling with the agreed names.

## Workflow detail

Dev payment runs on a `test_mode` user submit to HPBC against a staging SKU (`TOM-001_staging`, `TOM-002_staging`). Live SKUs are only used for the agreed go-live orders. Live SKU strings are to be confirmed with the supplier (Alex at Pureprint) and not derived by stripping `_staging`. Still to verify: `test_mode` flag reachability inside `hpbc_create_order` when the DB-trigger cascade fires.

## Related notes

- [[run-real-fulfilment-cascade-against-staging-sku]]
- [[separate-dev-prod-environments]]
- [[order-fulfilment-flow]]
- [[5-cto-implementation-plan]]
- [[2026-10-08-001]]
