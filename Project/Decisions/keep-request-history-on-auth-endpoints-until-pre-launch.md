---
type: decision
title: keep-request-history-on-auth-endpoints-until-pre-launch
project: tomale-rn-v1
status: accepted
date: 2026-10-23
related:
  - "[[2026-10-23-001]]"
  - "[[disable-request-history-on-credential-functions]]"
features:
  - X-security
  - F-auth
---

# Decision: keep-request-history-on-auth-endpoints-until-pre-launch

## What we decided

Request history stays on for the token-issuing auth endpoints while only test accounts exist. It is turned off before launch, and the item is on the pre-launch list.

## Why

Only test accounts exist, so the tokens captured in request history belong to test users. Recorded as an accepted risk at Phase 1 sign-off.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Issued tokens are kept in Xano request history until the pre-launch change. Accepted while there are no real users.

## Workflow detail

"Request history off on auth endpoints" sits on the pre-launch list alongside the `enforce_hidden_fields` sweep, rate limiting and the parental PIN. Distinct from [[disable-request-history-on-credential-functions]], which already turned history off on functions that send outbound API keys.

## Related notes

- [[2026-10-23-001]]
- [[disable-request-history-on-credential-functions]]
- [[defer-workspace-hidden-fields-setting-to-pre-launch-sweep]]
- [[add-per-endpoint-rate-limiting-in-xano]]
- [[6-api-security-model]]
