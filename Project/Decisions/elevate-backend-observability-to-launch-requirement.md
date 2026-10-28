---
type: decision
title: elevate-backend-observability-to-launch-requirement
project: tomale-rn-v1
status: accepted
date: 2026-07-14
features:
  - X-platform
---

# Decision: elevate-backend-observability-to-launch-requirement

## What we decided

Backend observability is now a launch requirement, not a Phase 2 nice-to-have. Since Xano has no native Sentry integration (confirmed with Xano support), backend error reporting must be built manually — Try/Catch blocks plus an External API Request to Sentry's event endpoint. This supersedes the Phase 2 "frontend minimum" wording in the CTO implementation plan §8.1 and Phase 2 task 15.

## Why

Webhook ingest, retry, and processing paths are backend-only and invisible to a frontend-only Sentry install. Launching without backend error reporting means money and fulfilment paths (Stripe payment confirmation, HPBC order status) can fail silently.

## Alternatives considered

Xano's native Error Logs plus its own alerting — costs nothing to build, but was explicitly rejected as a substitute rather than defaulted into, on the grounds that it doesn't give the same visibility as an external, alertable error-reporting pipeline for money and fulfilment paths.

## Trade-offs accepted

The manual Sentry integration (Try/Catch + External API Request per call site) is unestimated in the current plan — added scope not yet sized. Accepted because the alternative (silent failure on payment/fulfilment paths) is judged worse.

## Workflow detail

Supersedes CTO implementation plan §8.1 ("frontend minimum" observability) and Phase 2 task 15. Carried into "Next session" as its own work item (item 5: "Backend observability decision note"). No implementation done yet this session — this note records the requirement and the rejected alternative; the manual Sentry wiring itself is future work.

## Related notes

[[Sessions/2026-07-14-001]]
[[adopt-unique-index-dedup-for-webhook-ingest]]
[[adopt-uuid-primary-key-for-transaction-webhook-events]]
