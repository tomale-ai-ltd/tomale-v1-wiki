---
type: decision
title: ack-unknown-webhook-event-types-with-200
project: tomale-rn-v1
status: accepted
date: 2026-07-14
---

---

# Decision: ack-unknown-webhook-event-types-with-200

## What we decided

Webhook events of an unrecognized `event_type` are stored (ingested) and acknowledged with a bare 200 response, rather than rejected.

## Why

Stripe (and providers generally) retry any non-2xx response. Rejecting an unhandled event type would cause the provider to keep retrying the same delivery indefinitely — a retry storm — for an event the backend was never going to act on anyway.

## Alternatives considered

Rejecting unrecognized event types with a non-2xx response.

## Trade-offs accepted

Not discussed in session notes beyond the retry-storm rationale.

## Workflow detail

Implemented via the normalised internal event envelope (`domain` field: `order`/`subscription`) and a router with both branches; only the `order` branch is currently wired. Unknown types short-circuit to a 200 ack without hitting either branch, so no schema, ingest-function, or dedup-logic changes are needed when Apple/Google are added later.

## Related notes

[[Sessions/2026-07-14-001]]
[[differentiate-ingest-vs-processing-failure-responses-for-webhooks]] — same webhook response-contract session
[[adopt-unique-index-dedup-for-webhook-ingest]]
