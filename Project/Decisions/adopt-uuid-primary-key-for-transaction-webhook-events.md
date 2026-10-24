---
type: decision
title: adopt-uuid-primary-key-for-transaction-webhook-events
date: 2026-07-14
status: current
project: tomale-rn-v1
---

---

# Decision: adopt-uuid-primary-key-for-transaction-webhook-events

## What we decided

During the from-scratch rebuild of `transaction_webhook_events`, the primary key was switched from int to UUID.

## Why

Defensible for an internal-only table whose ids never reach a client — the table has no CRUD endpoints; all writes happen inside the webhook endpoints and the two shared custom functions (`webhook_event_ingest`, `webhook_event_complete`) via raw db blocks.

## Alternatives considered

An int primary key, as originally specified in `data-model.md`.

## Trade-offs accepted

This contradicts `data-model.md`, which still specifies int for this table. Whether the switch was a deliberate choice or a Xano default has not yet been confirmed — flagged as needing recording in the documentation refresh before it hardens.

## Workflow detail

`data-model.md` needs updating to reflect the UUID PK (carried into the "Next session" documentation refresh item alongside `api-spec.md`). No other endpoints or functions reference this table's primary key today, so the change is contained to this table.

## Related notes

[[Sessions/2026-07-14-001]]
[[adopt-unique-index-dedup-for-webhook-ingest]] — same rebuild, dedup mechanism for the same table
[[elevate-backend-observability-to-launch-requirement]] — same session, same milestone
