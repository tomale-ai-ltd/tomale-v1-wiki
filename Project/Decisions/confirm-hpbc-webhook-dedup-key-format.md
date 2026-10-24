---
type: decision
title: confirm-hpbc-webhook-dedup-key-format
date: 2026-07-15
status: current
project: tomale-rn-v1
---

---

# Decision: confirm-hpbc-webhook-dedup-key-format

## What we decided

The HPBC webhook dedup key is `hpbc:{hpbc_order_id}:{status}` on the success endpoint and `hpbc_error:{hpbc_order_id}:Error` on the error endpoint, following the existing shared dedup pattern (see [[adopt-unique-index-dedup-for-webhook-ingest]]). The field is `hpbc_order_id`, confirmed against a real captured payload — not `_id` as HPBC's documentation implied; the wrapper `_id` is HPBC's own log-record id and never reaches the endpoint. No `TimeStamp` is included in the key, since retries may not preserve it.

## Why

Payload field names were confirmed against a real callback rather than trusted from documentation, which caught the `_id` vs `hpbc_order_id` discrepancy before it shipped. Excluding `TimeStamp` from the key keeps retries of the same event correctly recognized as duplicates — including a timestamp would risk making legitimate retries look like distinct events.

## Alternatives considered

Keying on `_id` as HPBC's documentation implied — ruled out once the real payload showed `_id` is HPBC's own internal log-record id, not the order identifier. Including a `TimeStamp` in the key to distinguish otherwise-identical events — rejected because it reintroduces the retries-look-unique problem.

## Trade-offs accepted

Because both error triggers send `status: "Error"`, the error endpoint's key is always `hpbc_error:{hpbc_order_id}:Error` — a second, different error on the same order (e.g. a submission error followed by a production error) collides with the first and is swallowed as a duplicate. This was accepted deliberately: the customer-facing status is Error either way, support resolves from the HPBC dashboard, and only the second internal audit row is lost, not customer-visible state. The payload carries no field distinguishing the two error types, so preserving both would require adding a timestamp to the key, which reintroduces the retries-look-unique problem the key format is designed to avoid — judged not worth it.

## Workflow detail

Applies to both HPBC callback endpoints (`webhook_statusCallbackUrl`, `webhook_statusCallbackUrl_Error`), reusing the shared `webhook_event_ingest` / `webhook_event_complete` dedup pattern established for Stripe. All four test cases pass on each endpoint.

## Related notes

[[Sessions/2026-07-15-001]]
[[adopt-unique-index-dedup-for-webhook-ingest]] — shared dedup mechanism this decision extends to HPBC
[[authenticate-hpbc-webhooks-with-shared-secret-bearer-token]] — same endpoints, auth mechanics
[[scope-hpbc-callbacks-to-six-customer-facing-statuses]] — same endpoints, status surface
