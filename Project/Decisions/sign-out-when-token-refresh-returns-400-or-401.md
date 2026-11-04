---
type: decision
title: "sign-out-when-token-refresh-returns-400-or-401"
project: tomale-rn-v1
status: accepted
date: "2026-11-04"
related:
  - "[[2026-11-04-001]]"
  - "[[use-axios-401-interceptor-for-client-auth-session-handling]]"
  - "[[return-401-invalid-refresh-token-from-auth-refresh]]"
  - "[[store-token-issue-time-on-every-refresh]]"
affects:
  - "specs/007-foundations-session/spec.md"
features:
  - F-auth
---

# Decision: sign-out-when-token-refresh-returns-400-or-401

## What we decided

In client session handling (speckit 007), a token refresh refused with a 400 or 401 signs the user out, not only the `invalid_refresh_token` case. Network errors and 5xx responses keep the user signed in. Cursor applied the same sign-out to every other refresh failure, including a successful response that omits replacement credentials, so a broken refresh cannot leave later requests failing. Claude's plan review adds that 429 and timeouts are treated like network/5xx errors (stay signed in); carried into `/speckit.tasks`.

## Why

Raised in Claude's review of the 007 spec and taken to `/speckit.clarify` by Kyle. A broken refresh should not leave the app in a state where every later request fails.

## Alternatives considered

Signing out only on `invalid_refresh_token`, as in [[use-axios-401-interceptor-for-client-auth-session-handling]]. Not otherwise discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Recorded in the `## Clarifications` section of `specs/007-foundations-session/spec.md` (uncommitted on branch `007-foundations-session` at the time). Sign-out is client-only for now: there is no Xano `auth/logout`, so the refresh token stays valid on the server until it expires (tracked in [[pre-launch-checklist]] §1). This refines the sign-out trigger in [[use-axios-401-interceptor-for-client-auth-session-handling]].

## Related notes

- [[2026-11-04-001]]
- [[use-axios-401-interceptor-for-client-auth-session-handling]]
- [[return-401-invalid-refresh-token-from-auth-refresh]]
- [[store-token-issue-time-on-every-refresh]]
- [[pre-launch-checklist]]
