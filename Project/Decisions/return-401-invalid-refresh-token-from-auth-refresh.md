---
type: decision
title: "return-401-invalid-refresh-token-from-auth-refresh"
date: 2026-10-21
status: current
project: tomale-rn-v1
---

---

# Decision: return-401-invalid-refresh-token-from-auth-refresh

## What we decided

`auth/refresh` returns 401 with payload `invalid_refresh_token` for invalid or reused refresh tokens, replacing the two early 200 returns with 401 preconditions. Also fixed `!==` to `!=`. Published as `auth_refresh_2026-10-21.xs` (same `guid`). Postman covers it: 1D (valid refresh rotates token) returns 200, 1E (reused token) returns 401 `invalid_refresh_token`.

## Why

The client interceptor needs a distinguishable 401 to know when to clear the session and redirect to login. `user sessions.refresh_token` is confirmed password-type (hashed), so the `check_password` comparison is valid.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Any client code expecting a 200 from `auth/refresh` on failure will break; the on-hold frontend branch needs checking for this.

## Workflow detail

Postman 1A saves `refreshToken` for the 1D/1E tests. `6-api-security-model` is to be updated before Phase 1 sign-off.

## Related notes

- [[use-axios-401-interceptor-for-client-auth-session-handling]]
- [[use-expo-secure-store-for-client-tokens]]
- [[6-api-security-model]]
- [[7. Auth - Xano]]
- [[2026-10-21-001]]
