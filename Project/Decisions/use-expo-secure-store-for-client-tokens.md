---
type: decision
title: "use-expo-secure-store-for-client-tokens"
date: 2026-10-21
status: current
project: tomale-rn-v1
---

---

# Decision: use-expo-secure-store-for-client-tokens

## What we decided

Client auth tokens are stored in `expo-secure-store` instead of AsyncStorage. This settles the "future hardening decision" left open in `9. AsyncStorage.md` and deviates from the stack docs, which put tokens in AsyncStorage.

## Why

The stack docs flagged SecureStore as a future hardening step; the vault check on 2026-10-21 found the constitution and stack docs in conflict on client auth, and this resolves it in favour of the hardened option.

## Alternatives considered

Keep tokens in AsyncStorage (the current stack-doc position), with SecureStore deferred as later hardening.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Docs need updating: `9. AsyncStorage.md` describes the on-hold frontend branch, which should be checked for `auth/refresh` usage expecting a 200. Tracked in the documentation refresh backlog.

## Related notes

- [[use-axios-401-interceptor-for-client-auth-session-handling]]
- [[return-401-invalid-refresh-token-from-auth-refresh]]
- [[place-frontend-development-on-hold]]
- [[documentation-refresh-backlog]]
- [[6-api-security-model]]
- [[2026-10-21-001]]
