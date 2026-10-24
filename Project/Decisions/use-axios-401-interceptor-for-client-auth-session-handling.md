---
type: decision
title: "use-axios-401-interceptor-for-client-auth-session-handling"
date: 2026-10-21
status: current
project: tomale-rn-v1
---

---

# Decision: use-axios-401-interceptor-for-client-auth-session-handling

## What we decided

Client session handling uses a single Axios response interceptor on 401: one shared refresh across concurrent requests, one retry of the original request, and never triggered for `/auth/*` endpoints (so `/auth/refresh` cannot loop). On `invalid_refresh_token` the client clears tokens, resets the Zustand auth store, and the Expo Router root layout redirects to login. Network errors do not log the user out. The client also refreshes proactively on foreground, before the 1-hour token expiry.

## Why

The constitution requires Axios interceptors. Excluding `/auth/refresh` from the retry avoids a refresh loop, and separating `invalid_refresh_token` from network errors prevents spurious logouts.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Frontend is on hold, so this is the spec for when it resumes. Depends on the backend returning 401 `invalid_refresh_token` from `auth/refresh`.

## Related notes

- [[return-401-invalid-refresh-token-from-auth-refresh]]
- [[use-expo-secure-store-for-client-tokens]]
- [[place-frontend-development-on-hold]]
- [[7. Auth - Xano]]
- [[2026-10-21-001]]
