---
type: decision
title: authenticate-hpbc-webhooks-with-shared-secret-bearer-token
project: tomale-rn-v1
status: accepted
date: 2026-07-15
---

---

# Decision: authenticate-hpbc-webhooks-with-shared-secret-bearer-token

## What we decided

The HPBC webhook endpoints (`webhook_statusCallbackUrl` and `webhook_statusCallbackUrl_Error`) are public endpoints with in-stack bearer token verification as the sole guard, rather than Xano auth-table (user account/JWT) authentication. Pre-existing auth code was fixed: it was returning `badrequest` (a 400) while claiming to be a 401, now corrected to `unauthorized`; the endpoint also no longer leaks the internal function result in the response.

## Why

HPBC is an external service with no user account or JWT to authenticate against, so Xano's normal auth-table authentication doesn't apply. This is the shared-secret webhook case that CTO implementation plan sections 2.1 and 2.6 explicitly allow. Because the in-stack bearer check is the sole guard on a public endpoint, it must be fail-closed and use a whole-string compare.

## Alternatives considered

Xano auth-table (user-account/JWT) authentication — not applicable since HPBC has no user account to authenticate as.

## Trade-offs accepted

Being the sole guard on a public endpoint places full weight on the bearer check being fail-closed and correctly implemented; this session found and fixed a case where the failure path was returning the wrong status code and leaking internal data. The token itself was pasted into working chat during this session and needs rotation (see "Blockers / questions" in the session note) to ensure the exposure doesn't carry forward.

## Workflow detail

Applies to both HPBC callback endpoints, built this session against a real captured payload. `hp_webhook_token` rotation is carried into "Next session": the new value must be set in both the Xano env var and the SiteFlow trigger configs so they stay in sync.

## Related notes

[[Sessions/2026-07-15-001]]
[[confirm-hpbc-webhook-dedup-key-format]] — same endpoints, dedup mechanics
[[scope-hpbc-callbacks-to-six-customer-facing-statuses]] — same endpoints, status surface
