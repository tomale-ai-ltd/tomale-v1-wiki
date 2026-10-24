---
type: decision
title: mark-order-error-on-hpbc-rejection-and-clear-lock
project: tomale-rn-v1
status: accepted
date: 2026-10-14
---

---

# Decision: mark-order-error-on-hpbc-rejection-and-clear-lock

## What we decided

When HPBC rejects an order, it is marked Error, and `hpbc_create_order` clears the lock on every failure path. It also sets Error on a non-2xx response and has request history off. Proposed in the pending `hpbc_create_order_2026-10-14b.xs`: failed pre-submit checks and timeouts also mark the order Error rather than retrying.

## Why

Marking failed pre-submit checks Error stops the background task retrying forever. Marking a timeout Error avoids a duplicate print, since the submission may have reached Pureprint.

## Alternatives considered

Automatic retry on timeout. Whether it is safe depends on Alex's answer on whether Pureprint rejects a repeated `sourceOrderId`.

## Trade-offs accepted

Timed-out orders need manual attention instead of automatic retry, until the `sourceOrderId` question is answered.

## Workflow detail

14b is drafted but not yet applied. Order 134 diagnosis checks `submit_after`, `status`, `hpbc_lock`, then `hpbc_order_id`.

## Related notes

- [[make-hpbc-create-order-a-single-fail-closed-request]]
- [[delay-hpbc-submission-with-30-minute-cancellation-window]]
- [[enforce-forward-only-hpbc-callback-status-transitions]]
- [[2026-10-14-001]]
