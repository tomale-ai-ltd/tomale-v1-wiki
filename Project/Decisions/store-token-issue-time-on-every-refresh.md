---
type: decision
title: "store-token-issue-time-on-every-refresh"
project: tomale-rn-v1
status: accepted
date: "2026-11-04"
related:
  - "[[2026-11-04-001]]"
  - "[[use-axios-401-interceptor-for-client-auth-session-handling]]"
  - "[[use-expo-secure-store-for-client-tokens]]"
affects:
  - "specs/007-foundations-session/spec.md"
features:
  - F-auth
---

# Decision: store-token-issue-time-on-every-refresh

## What we decided

The client stores the access token's issue time on every successful refresh, replacing the previous time, not only at sign-in. The 50-minute foreground refresh check then starts again from that refresh. Cursor's assumption, recorded with the clarification: a missing issue time (including a session moved from ordinary storage) counts as due for refresh, and that refresh then stores the issue time.

## Why

If the issue time were stored only at sign-in, the 50-minute foreground check would keep firing after the first refresh.

## Alternatives considered

Storing the issue time only at sign-in. Not otherwise discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Raised in Claude's review of the 007 spec; answered by Kyle in `/speckit.clarify` and recorded in the spec's `## Clarifications`. The 007 plan persists the session in Zustand via `expo-secure-store` (`AFTER_FIRST_UNLOCK`, chunked), memory on web.

## Related notes

- [[2026-11-04-001]]
- [[use-axios-401-interceptor-for-client-auth-session-handling]]
- [[use-expo-secure-store-for-client-tokens]]
- [[sign-out-when-token-refresh-returns-400-or-401]]
