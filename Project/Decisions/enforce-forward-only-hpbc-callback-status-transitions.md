---
type: decision
title: enforce-forward-only-hpbc-callback-status-transitions
project: tomale-rn-v1
status: accepted
date: 2026-10-14
features:
  - F-print-fulfilment
---

# Decision: enforce-forward-only-hpbc-callback-status-transitions

## What we decided

`hpbc_update_order` enforces transition rules. Statuses only move forward: Order Confirmed, In Production, Shipped. Error is accepted only before Shipped and can be recovered by a later forward status. Cancelled is accepted only before In Production and is terminal. Tracking is always merged. Callbacks with an empty `hpbc_order_id` or status are rejected. The response gains an `applied` flag. No new Print Ready status is added: In Production maps to Pureprint's Order Print Ready.

## Why

Pureprint's real trigger sequence (Order Errored, Received, Submission Error with retries for up to 24 h, Print Ready, Component Printed, Shipped, Cancelled) can deliver out-of-order or late callbacks. The guard stops them regressing an order's status.

## Alternatives considered

A separate Print Ready status was considered and rejected, since In Production equals Print Ready.

## Trade-offs accepted

Late Error callbacks after Shipped are ignored (3D-3 asserts the status stays Shipped). Component Printed gets no customer-facing status.

## Workflow detail

Published as `hpbc_update_order_2026-10-14.xs`. Kyle to check the In Production callback is attached to the "Order Print Ready" trigger. Postman 3D-3 needs a skip guard when `hpbcOrderId` is unset.

## Related notes

- [[scope-hpbc-callbacks-to-six-customer-facing-statuses]]
- [[delay-hpbc-submission-with-30-minute-cancellation-window]]
- [[mark-order-error-on-hpbc-rejection-and-clear-lock]]
- [[2026-10-14-001]]
