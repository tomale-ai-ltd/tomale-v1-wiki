---
type: decision
title: add-temporary-audit-trigger-on-store-orders
project: tomale-rn-v1
status: accepted
date: 2026-10-14
---

---

# Decision: add-temporary-audit-trigger-on-store-orders

## What we decided

Added an `audit_store_orders` table and an `audit_store_orders_changes` update trigger as a temporary diagnostic. It records `old_values`, `new_values`, `diff`, `changed_fields`, `request_method`, `request_uri` and `user_id` (read only when an auth context exists). It stays internal with no endpoint. Whether to keep it as a permanent audit trail, with a retention period, is decided in the Phase 2 observability work.

## Why

`store_orders.created_at` is confirmed to change in the database. Every function that writes to orders was reviewed (all partial edits, none write `created_at`) and a Xano bot audit agreed, but the root cause was not found. Xano has no record-level history (Compliance Center tracks schema and objects only).

## Alternatives considered

Code review of all order-writing functions, which found nothing.

## Trade-offs accepted

The table holds shipping personal data, so it is internal-only and its retention needs deciding.

## Workflow detail

Read the `audit_store_orders` rows after the next run to close the investigation.

## Related notes

- [[elevate-backend-observability-to-launch-requirement]]
- [[2026-10-14-001]]
