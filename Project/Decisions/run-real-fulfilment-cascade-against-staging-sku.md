---
type: decision
title: run-real-fulfilment-cascade-against-staging-sku
project: tomale-rn-v1
status: accepted
date: 2026-10-08
---

---

# Decision: Run the Real Fulfilment Cascade Against a Staging SKU Instead of Simulating HPBC

## What we decided

The order-fulfilment flow test runs the real DB-trigger cascade end to end (`order_fulfilment_check` → `reconcile_order_fulfilment` → `hpbc_create_order`) against a `_staging` SKU. We do not simulate the HPBC callback, and there is no sandbox to use instead.

## Why

HPBC has no sandbox. The `_staging` SKUs route to the live Brand Centre, run print-file checks, and are rejected before production. That is the only way to exercise HPBC's print-file preflight on our PDFs, which is the one thing worth proving. Fulfilment is also a DB trigger, not an endpoint call, so a payment run auto-submits to HPBC with no natural seam to stop at. A simulate branch would skip the preflight check. Pureprint confirmed that staging orders incur no HPBC charge.

## Alternatives considered

- **HPBC sandbox** — not available.
- **Simulated callback** — rejected because it skips the preflight check.

## Trade-offs accepted

The terminal status of a valid staging order is unknown until run 1. The expectation is Cancelled, but HPBC decides, so assertion `C1b` stays commented until run 1 confirms it. Runs submit real orders to the live Brand Centre, though rejected before production.

## Workflow detail

The flow test is three async-gated phases: A (drive to payment), B (PDFs and cascade), C (HPBC terminal state). Run 1 doubles as discovery of the staging terminal status. The folder runs once per staging SKU (`TOM-001_staging`, `TOM-002_staging`), and Alex at Pureprint is told the `order_number`s once staging orders are sent. Go-live sequence agreed with Pureprint: staging orders on both SKUs, Alex confirms, one order per live SKU (real print, real cost), then production opens.

## Related notes

- [[key-hpbc-environment-switch-off-stripe-test-mode]]
- [[order-fulfilment-flow]]
- [[5-cto-implementation-plan]]
- [[2026-10-08-001]]
