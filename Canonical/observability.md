---
type: living-doc
title: observability
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-10-24
last_verified: 2026-10-28
owner: vault
related:
  - "[[stack]]"
  - "[[backend-xano]]"
  - "[[pre-launch-checklist]]"
---

# Observability

How we find out that something broke, across the app and the backend. The decision that sets the bar: backend observability is a **launch requirement**, because the money and fulfilment paths run only in the backend and would otherwise fail silently ([[elevate-backend-observability-to-launch-requirement]]).

## 1. App (frontend)

| What | How | Status |
|---|---|---|
| Crashes, runtime errors, failed API calls | `@sentry/react-native`, DSN from `EXPO_PUBLIC_SENTRY_DSN`, environment `development` / `production` | Built (004) |
| PII scrubbing | `beforeSend` hook; root `Sentry.ErrorBoundary` with a friendly fallback (constitution, Principle 5) | Built |
| Context on events | User id, active profile id, feature, entity id (CTO §8.2, **CTO #16**) | To do (M1) |
| Source maps | Uploaded by CI for production releases (release `<version>+<shortsha>`) | To do with release setup |
| OTA updates | `expo-updates` with EAS channels | Configured (004) |

## 2. Backend (Xano)

| What | How | Status |
|---|---|---|
| Request and function history | Xano history, 100 per item by default; 0 on functions that send API keys ([[disable-request-history-on-credential-functions]]); `auth/login` keeps 100 until pre-launch | In use. Retention: function runs 24 h, background tasks 7 days |
| Pipeline runs | `executor_runs` (small status fields only, found by id) for image and PDF executors | In use |
| Webhook events | `transaction_webhook_events`: every Stripe and HPBC event stored before processing, with a status | In use |
| Order changes | `audit_store_orders` trigger (temporary diagnostic) | In use; keep or remove before launch |
| User activity | `user_logs` | In use |
| Error reporting | Try/catch + External API Request to Sentry's event endpoint on webhooks, executors, fulfilment, refunds. Xano has no native Sentry integration (confirmed with Xano support) | **To build** (M9, **CTO #15**) |
| Alerting | Email on repeated errors and spikes (**CTO #17**) | **To build** (M9) |
| Reading history in bulk | Metadata API (filters as query-string parameters) with the read-only `cursor-read` token | Available |

## 3. End-to-end checks

- Postman `_tests` after every backend change; a daily monitor at launch ([[test-suite]]).
- Folder 1 test 1C fails if any story is stuck in a non-terminal state longer than 45 minutes.
- Reconciliation tasks: `reconcile_order_refunds`, `reconcile_stripe_customers`.

## 4. What to log (CTO §8.4)

Key backend events only: story generation started and failed, moderation result, payment success and failure, HPBC submission and callbacks, refunds. No full payloads, keys or images in logs ([[log-only-small-status-fields-in-executor-runs]]).
