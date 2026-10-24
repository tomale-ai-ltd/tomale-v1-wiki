---
type: decision
title: replace-manual-test-gates-with-bounded-polling
project: tomale-rn-v1
status: accepted
date: 2026-10-09
---

---

# Decision: Replace Manual Flow-Test Gates with Bounded Polling

## What we decided

The PDF-ready gate (B1 / 3C-2) and the HPBC terminal-status gate (C1 / 3D-3) are polling loops with bounded attempts: fail fast on order status `Error`, hard fail on timeout.

- **3C-2:** polls until `cover_pdf.url` and `inner_pdf.url` are both present; asserts `payment_status = Confirmed` once at the end. Defaults 8 × 15s (`b1MaxAttempts`, `b1PollDelayMs`).
- **C1 (now 3D-1):** polls `store_orders.status` until terminal. Pass on `Order Confirmed` (or `Cancelled` if cancelled manually); fail fast on `Error` or a non-200 response. Defaults 10 × 20s (`c1MaxAttempts`, `c1PollDelayMs`); the counter resets when `orderId` changes.
  - *Updated 2026-10-13:* Pureprint (Alex) confirmed staging orders stay at `Order Confirmed` unless manually cancelled, so the original `Cancelled` assumption would always time out.

Loops use `setTimeout` in the pre-request script and `pm.execution.setNextRequest(pm.info.requestName)`.

## Why

Manual gates prevent unattended runs. Bounded polling lets the collection run end to end without human input, while the cap and fail-fast behaviour stop it hanging on a failed order.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

`setNextRequest` looping only works in the Collection Runner, Newman and monitors, not single sends. Waits add up (~2 min + ~3.3 min if both polls run in one monitor). The C1 terminal status is now confirmed by Pureprint (`Order Confirmed` for staging).

## Workflow detail

Single-request sends of 3C-2 and 3D-3 do not loop. The C1 assertion is locked to `Order Confirmed` (2026-10-13). Simulated HPBC callbacks (3D-2 lifecycle: In Production → Shipped with tracking; 3D-3 error) run after C1 so they cannot change status before it is checked. Monitor setup is to be decided separately (run-time limit and secret-variable availability unverified).

## Related notes

- [[simulate-stripe-payment-with-signed-postman-webhook]]
- [[use-fixture-story-for-order-flow-test]]
- [[run-real-fulfilment-cascade-against-staging-sku]]
- [[order-fulfilment-flow]]
- [[2026-10-09-001]]
