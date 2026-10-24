---
type: decision
title: "disable-request-history-on-credential-functions"
date: 2026-10-14
status: current
project: tomale-rn-v1
---

---

# Decision: disable-request-history-on-credential-functions

## What we decided

Request history is set to 0 on the functions that send API keys: `hpbc_create_order`, `reconcile_order_fulfilment`, both Papermill functions, and the refund function.

## Why

Request history would otherwise store outbound API keys.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Debugging is harder: failures in these functions leave no request history. Task history is also off, which hid the cause of order 134 not being submitted, so it is to be turned on temporarily when diagnosing.

## Workflow detail

Apply to any new function that sends credentials.

## Related notes

- [[elevate-backend-observability-to-launch-requirement]]
- [[delay-hpbc-submission-with-30-minute-cancellation-window]]
- [[2026-10-14-001]]
