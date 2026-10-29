---
type: prd
title: PRD-transaction-webhooks-micro-prd
project: tomale-rn-v1
status: current
version: 2.0
date: 2026-04-14
last_verified: 2026-10-29
owner: vault
features:
  - F-payments
  - F-subscriptions
related:
  - "[[PRD-Subscription-Entitlement-System]]"
  - "[[security-model]]"
  - "[[backend-xano]]"
---

# MICRO-PRD: Transaction Webhooks & Billing Event Processing

> **Reviewed and approved by Kyle (29/10):** subscriptions come through **RevenueCat** for Apple and Google ([[use-revenuecat-for-in-app-subscriptions]]); one RevenueCat webhook replaces separate Apple and Google endpoints; Stripe subscriptions move to V2 with Club ([[v2-backlog]]).
>
> **Changes in 2.0 (B9, 29/10/2026):** split into what's **built** (book-order payments, refunds and HPBC callbacks on the shared ingest pattern) and what's **to build** for subscriptions (Stripe mode branching, Apple, Google). Endpoint names, dedup and failure responses match the live `webhooks` group and its decisions.

## Goal
A reliable, provider-agnostic webhook ingestion system that:
- processes billing events from Stripe (books) and RevenueCat (subscriptions), and print events from HPBC
- keeps orders and subscription state accurate
- triggers entitlement recalculation
- keeps every event for audit and replay

## Core Concepts (non-negotiable)
- Webhooks are the **source of truth for billing state**.
- Every payload is **stored before processing**.
- Processing is **idempotent**.
- Provider events are **normalised** into internal events.
- Ingestion **fails safely and is retryable**.

## Built (live `webhooks` group)

| Endpoint | Caller | Verification | Handles |
|---|---|---|---|
| `POST /stripe/webhook_payment_confirmation` | Stripe | Signature | `checkout.session.completed` for book orders; refund events |
| `POST /hpbc/webhook_statusCallbackUrl` | HPBC/Pureprint | Bearer token | Order Confirmed, In Production, Shipped, Cancelled |
| `POST /hpbc/webhook_statusCallbackUrl_Error` | HPBC/Pureprint | Bearer token | Error |

**Pattern (shared functions `webhook_event_ingest` / `webhook_event_complete`):**
1. Verify the caller (Stripe signature or HPBC bearer token); fail → opaque 401.
2. Ingest: insert into `transaction_webhook_events` with a computed `dedup_key` under a unique index; a duplicate is caught and acknowledged without reprocessing ([[adopt-unique-index-dedup-for-webhook-ingest]]). Dedup keys: Stripe event id; HPBC `hpbc:{order}:{status}` and `hpbc_error:{order}:Error` ([[confirm-hpbc-webhook-dedup-key-format]]).
3. Process, then mark the event `success` or `failed`.
4. Responses ([[differentiate-ingest-vs-processing-failure-responses-for-webhooks]]): ingest failure → 500 so the provider retries; processing failure → 200, marked `failed`, retried internally from the stored payload. Unknown event types are stored and acknowledged with 200 ([[ack-unknown-webhook-event-types-with-200]]).

**`transaction_webhook_events`** (live): `id` (uuid), `provider` (indexed text), `users_id`, `external_id`, `event_type`, `dedup_key` (unique), `status` (pending, success, failed), `retry_count`, `processing_errors`, `payload`, `processed_at`, timestamps. Money facts go to `transactions`, never here ([[split-webhook-ingress-log-from-money-transactions]]).

## To build (subscriptions, [[roadmap]] M8)

### RevenueCat webhook
`POST /revenuecat/webhook` in the `webhooks` group, on the shared ingest pattern:
1. **Verify:** RevenueCat sends a fixed `Authorization` header value set in its dashboard; compare it with an environment variable (constant-time). Fail → opaque 401.
2. **Ingest:** `provider = revenuecat`, `dedup_key = revenuecat:{event.id}`, `external_id` = the app user id, `event_type` = the RevenueCat type.
3. **Process:** treat the event as a trigger, not as the state. Look up the user by `revenuecat_app_user_id` and run `revenuecat_sync_subscriber` ([[PRD-Subscription-Entitlement-System]]), which fetches the subscriber from RevenueCat and overwrites the mirror. Order and duplicates then don't matter.
4. Events from the sandbox environment only change users in `test_mode`, and production events only change users not in test mode.

| RevenueCat event (to confirm against its docs when built) | Effect after the sync |
|---|---|
| `INITIAL_PURCHASE` (including trial start) | Subscription created: trial or active |
| `RENEWAL` (including trial → paid) | Period extended, active |
| `CANCELLATION` | Auto-renew off (or refunded); access to period end unless refunded |
| `UNCANCELLATION` | Auto-renew back on |
| `BILLING_ISSUE` | Grace or past_due; new generation blocked |
| `EXPIRATION` | Expired → Free |
| `PRODUCT_CHANGE` | Monthly ↔ annual |
| `TRANSFER` | Moves to another account (limited by the transfer setting) |
| `TEST` | Stored and acknowledged |
| Anything else | Stored and acknowledged with 200 ([[ack-unknown-webhook-event-types-with-200]]) |

### Stripe
No change in V1: the handler stays book-orders only. Branching on `mode` for Stripe subscriptions moves to V2 with Club ([[defer-stripe-webhook-mode-branching-to-phase-2]], amended 29/10).

### Processing rules
- Only the sync function knows RevenueCat; the entitlement gate reads the mirror.
- After each sync, `GET /me/entitlements` reflects the change (resolved at request time, nothing to recalculate).

## Backend prep (from the generated [[Repos/tomale-rn-test/memory/data-model|data-model]] and the live `webhooks` group)
**Live:** `transaction_webhook_events`, `webhook_event_ingest` / `webhook_event_complete`, the Stripe and HPBC endpoints, `reconcile_order_refunds`, `reconcile_stripe_customers`.

**To build:**
1. `POST /revenuecat/webhook` (above), with `REVENUECAT_WEBHOOK_AUTH` and `REVENUECAT_SECRET_KEY` as environment variables, separate for dev and prod branches.
2. The `revenuecat` provider value and dedup key format, recorded in [[backend-xano]].
3. Sandbox/production routing by `test_mode`.
4. Sentry reporting on the new endpoint ([[observability]]).
5. **Postman `_tests`:** wrong auth → 401 and nothing stored; a duplicate event → processed once; an unknown type → 200; a sample `INITIAL_PURCHASE` → mirror updated (sync stubbed or against the RevenueCat sandbox).

## Error handling and retries
- Invalid signature → reject (401), nothing stored.
- Malformed payload → stored, marked failed.
- Processing error → retried from the stored payload (`retry_count`, maximum configurable).
- Reconciliation tasks catch anything missed (`reconcile_order_refunds`, `reconcile_stripe_customers`; the daily RevenueCat sync from [[PRD-Subscription-Entitlement-System]]).

## Observability
Backend errors on webhook paths report to Sentry (launch requirement, [[observability]]). Track events received, success vs failure, retries and latency.

## Acceptance Criteria
- Every event is stored before processing.
- Duplicates never change state twice.
- Subscription state reflects the latest valid event.
- Entitlements update after processing.
- Failed events can be retried safely.
- Subscription state comes only from RevenueCat syncs, never from interpreting a single event.
