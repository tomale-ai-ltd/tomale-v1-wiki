# 007-foundations-session -- Client session handling -- Secure tokens, one 401 interceptor, Sentry context #

<!--
Micro-PRD for speckit 007 (M1 PR D). Drafted by Claude 04/11 from the decisions below and the 03/11 repo read.
Cursor copies it to `.docs/prd/007-foundations-session.md` before `/speckit.specify`.
Sources: [[use-expo-secure-store-for-client-tokens]], [[use-axios-401-interceptor-for-client-auth-session-handling]],
[[return-401-invalid-refresh-token-from-auth-refresh]], [[use-https-web-intermediary-for-magic-link-redirect]], constitution 1.6.0, CTO #16.
-->

## Goal

Signed-in sessions survive normally and securely. Tokens live in the device keychain, every API call carries the token automatically, an expired access token is refreshed once and the call retried, and the user is only signed out when the refresh token is truly invalid. Crash reports identify the user and profile. No visible UX change except that the Bookshelf loads (today it gets 401 because no token is sent).

## Screen flow

- `app/(auth)/login.tsx`, `app/(auth)/send-login-link.tsx` (store tokens on success)
- `app/auth/complete.tsx` (magic-link completion)
- `app/_layout.tsx` (auth gate, app foreground handling)

**Navigation rules:**

- Login, signup or magic-link success → tokens stored → `(main)`.
- Refresh fails with 401 `invalid_refresh_token` → logout → `(auth)/login`.
- Network error or 5xx during refresh → stay signed in, show the call's error.

## Scope (this slice only)

- `expo-secure-store` for `authToken`, `refreshToken`, `userId`, `sessionId`, token issue time (`AFTER_FIRST_UNLOCK`); one-time migration from the AsyncStorage `auth` key, then delete it. Web: memory only.
- Capture `refreshToken` and `session_id` from `auth/login`, `auth/signup`, `auth/complete_magic_link`.
- `api/http.ts` rebuilt on Axios (already a dependency), keeping today's error shape plus the payload `code`. Request interceptor attaches the bearer; remove hand-written `Authorization` headers.
- Response interceptor: 401 on a non-`/auth/*` call → one shared `POST /auth/refresh` → store rotated tokens → retry once.
- Foreground: refresh first if the token is older than 50 minutes.
- `auth/complete.tsx`: remove the `authToken` URL-parameter path (tokens never travel in URLs).
- Sentry: `setUser({ id })` on sign-in, `null` on logout; `profile_id` tag; `beforeSend` keeps `user.id`, strips email, username, IP.
- First commit: RS-2026-11-04-01 (remove the `@swc/helpers` override once 0.5.24 is 7 days old).

## Out of scope

- Profile switching UI and parental PIN (M3); Universal Links; Xano changes.

## State Management

`store/AuthStore.ts` persists through a SecureStore-backed Zustand storage adapter; the HTTP layer reads tokens from the store and writes rotated ones back.

## Endpoints (contracts provided separately)

POST /auth/refresh → 200: { authToken, refreshToken, userid } (body: users_id, refreshToken)

Error: 401 invalid_refresh_token

GET /instant_stories → 200: Story[] (Bookshelf, now authenticated)

## Acceptance (Given/When/Then)

Happy path

- Given a signed-in user whose access token has expired
- When the Bookshelf loads
- Then one refresh happens, the request is retried, and stories show

Edge

- Given three calls fail with 401 at once
- When the interceptor runs
- Then exactly one refresh request is made and all three retry once

Error

- Given refresh returns 401 `invalid_refresh_token`
- When any protected call is made
- Then the user is logged out to Sign in; a network error instead keeps them signed in

Device checks (Kyle, EAS dev build): sign in, kill and reopen (still signed in); legacy AsyncStorage session migrates; a dev-only test error reaches Sentry with `user.id` and `profile_id`.
