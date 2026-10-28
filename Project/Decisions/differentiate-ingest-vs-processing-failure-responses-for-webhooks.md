---
type: decision
title: differentiate-ingest-vs-processing-failure-responses-for-webhooks
project: tomale-rn-v1
status: accepted
date: 2026-07-14
features:
  - F-payments
  - F-print-fulfilment
---

# Decision: differentiate-ingest-vs-processing-failure-responses-for-webhooks

## What we decided

Webhook failures return two different response codes depending on where they occur. An ingest failure (the event was never stored) returns 500 so the provider retries the delivery. A processing failure (the event was already stored) returns 200, marks the event `failed` via `webhook_event_complete`, and is retried internally from the stored payload rather than relying on the provider to redeliver.

## Why

The two failure modes have different durability guarantees. If the event never made it into `transaction_webhook_events`, the only copy of it is the provider's queued delivery, so it must be told to retry (500). If the event is already durably stored, the backend owns retry from that point on — telling the provider to redeliver would just create a duplicate that dedup then has to absorb again.

## Alternatives considered

Not explicitly discussed in session notes; the implicit alternative is a single response code for all failure types regardless of whether the event was durably stored.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Relies on the `status` field on `transaction_webhook_events` (indexed for the retry-sweep filter) and the `retry_count` / `processing_errors` fields set by `webhook_event_complete`. Internal retry from stored payload is the mechanism for processing failures going forward for any provider using the shared ingest/complete functions.

## Related notes

[[Sessions/2026-07-14-001]]
[[ack-unknown-webhook-event-types-with-200]] — same webhook response-contract session
[[adopt-unique-index-dedup-for-webhook-ingest]]
