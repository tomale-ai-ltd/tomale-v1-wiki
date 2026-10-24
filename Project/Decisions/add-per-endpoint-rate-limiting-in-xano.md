---
type: decision
title: "add-per-endpoint-rate-limiting-in-xano"
date: 2026-10-21
status: current
project: tomale-rn-v1
---

---

# Decision: add-per-endpoint-rate-limiting-in-xano

## What we decided

Use per-endpoint Rate Limit functions in Xano, covering auth, order create/cancel, and story/image generation. Phase 2 before launch is recommended; the phase is still to be confirmed. The pre-launch checklist also includes a rate-limit pre-middleware by IP on the `app` group, after checking that `$env.$remote_ip` is the real client IP.

## Why

Xano paid plans have no platform-level rate limit, so protection must be built into the endpoints.

## Alternatives considered

Relying on a platform-level limit, which is not available on Xano paid plans.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Added to the Xano pre-launch checklist (Phase 2: endpoint inventory, rate-limit pre-middleware, test-data cleanup, CORS, backup). Phase 1 quick settings are separate: Swagger private, sensitive data flags, 2FA, remove unused metadata tokens.

## Related notes

- [[6-api-security-model]]
- [[adopt-rebac-auth-model]]
- [[2026-10-21-001]]
