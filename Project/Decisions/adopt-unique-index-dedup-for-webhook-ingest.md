---
type: decision
title: adopt-unique-index-dedup-for-webhook-ingest
date: 2026-07-14
status: current
project: tomale-rn-v1
---

---

# Decision: adopt-unique-index-dedup-for-webhook-ingest

## What we decided

Deduplication for `transaction_webhook_events` is enforced via a unique index on a computed `dedup_key`, paired with an insert-and-catch pattern in the shared `webhook_event_ingest` custom function: the function inserts the raw event, and if the unique constraint is violated, the catch branch looks up the existing row and returns `is_duplicate: true` with the same event id. Dedup key composition (e.g. `stripe:{id}`) stays inline in each provider's endpoint rather than living inside the shared function.

## Why

Insert-and-catch was chosen over query-then-insert to close the race window where two concurrent copies of the same event both see "not found" and both insert. A unique index makes Postgres itself arbitrate the conflict, which is race-safe in a way an application-level check-then-write cannot be. This session confirmed (rather than assumed) that Xano's Try/Catch does catch a unique-constraint violation instead of aborting the whole stack, which is what makes the pattern viable. Keeping key composition inline per provider (instead of a provider switch inside the shared function) keeps the shared function generic — a provider switch inside it would defeat the point of sharing it.

## Alternatives considered

A raw composite index (e.g. on `provider` + `external_id`) instead of a computed `dedup_key`.
Query-then-insert (check for an existing row, then insert if absent) instead of insert-and-catch.

## Trade-offs accepted

The approach depends on Xano's Try/Catch reliably catching unique-constraint violations rather than failing the request outright — confirmed working this session, but a dependency on that specific behavior nonetheless. Not otherwise discussed in session notes.

## Workflow detail

Both shared functions (`webhook_event_ingest`, `webhook_event_complete`) are used by every provider wired into the webhook router (currently Stripe's `stripe:{id}` and HPBC's `hpbc:`/`hpbc_error:` namespaces), so this pattern is the dedup mechanism for all current and future webhook providers, not just Stripe.

## Related notes

[[Sessions/2026-07-14-001]]
[[Sessions/2026-07-03-001]] — initial scoping of `transaction_webhook_events` as a generic provider ingress log
[[adopt-uuid-primary-key-for-transaction-webhook-events]] — same rebuild, same table
