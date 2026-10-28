---
type: decision
title: avoid-recreating-removed-endpoints-for-testing
project: tomale-rn-v1
status: accepted
date: 2026-10-09
features:
  - X-testing
---

# Decision: Don't Recreate Removed Endpoints for Testing

## What we decided

Endpoints removed in the API cleanse are not brought back to support the flow test. Outcomes are asserted through existing user-facing endpoints (order status / paid). `3D-1 GET /transaction_webhook_events` and `3D-2 GET /store_order_updates` were deleted from the collection; their intent is covered by the paid-status check after 3B-2 and the C1 terminal-status poll. If ingest/dedup rows ever need asserting, add read-only, auth + admin-gated GETs in a dev-only testing API group. Never add a write or simulate endpoint in a group that ships to prod.

## Why

The endpoints were removed deliberately in the API cleanse; reintroducing them for tests would undo that and widen the production surface. The removed requests asserted internal records that are already evidenced by the order's observable status.

## Alternatives considered

- **Recreate the endpoints** — rejected (above).
- **Test-only simulate/write endpoint** — rejected; only read-only, admin-gated GETs in a dev-only group are allowed if ever needed.

## Trade-offs accepted

Webhook-event and HPBC update rows are not asserted directly; the tests rely on downstream order status as proof.

## Workflow detail

The `_tests` collection contains no requests against removed endpoints, and the `store_order_updates` wording was removed from 3D-3.

## Related notes

- [[simulate-stripe-payment-with-signed-postman-webhook]]
- [[replace-manual-test-gates-with-bounded-polling]]
- [[remove-user-activities-endpoint]]
- [[adopt-unique-index-dedup-for-webhook-ingest]]
- [[6-api-security-model]]
- [[2026-10-09-001]]
