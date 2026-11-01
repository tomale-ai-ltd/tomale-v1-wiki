---
type: brief
title: m1-cursor-briefs
project: tomale-rn-v1
status: draft
date: 2026-11-01
related:
  - "[[roadmap]]"
  - "[[repo-sync]]"
---

# M1 app foundations rework: Cursor briefs

Four PRs into `main`, in order. Each must pass the required `test` check. Cursor applies only items Kyle has marked `approved` in [[repo-sync]], and writes a raw note to `_raw/Chat Sessions/` at the end.

---

## PR A: tooling and CI (`repo-sync/2026-11-01-tooling`)

Items: RS-2026-10-30-03 (Node 22), RS-2026-10-30-05 (Renovate), RS-2026-11-01-02 (CI security stage), RS-2026-11-01-05 (Cursor rule: repo-sync process).

Prompt for Cursor:

> Apply repo-sync items RS-2026-10-30-03, RS-2026-10-30-05, RS-2026-11-01-02 and RS-2026-11-01-05 from `Canonical/repo-sync.md` in the tomale-v1-wiki folder, on branch `repo-sync/2026-11-01-tooling`, one commit per item, prefixed with the item id.
> - Node 22: `.nvmrc` → latest Node 22 LTS (at least 22.13, which Expo SDK 58 needs); `package.json` engines → `>=22.13 <23`. Confirm the current app and pnpm 10.34.7 work on it.
> - Renovate: `renovate.json` with monthly grouped updates, `minimumReleaseAge` 7 days, security updates immediately, Expo SDK packages (`expo`, `expo-*`, `react-native`, `react`, `react-native-reanimated`, `react-native-worklets`) in one group that is never auto-merged. No auto-merge anywhere.
> - CI: add Gitleaks (CLI) and Semgrep OSS (ERROR severity only) as steps inside the existing `test` job; remove the wip branch from the trigger.
> Don't touch app code, Xano files, `api/openapi`, `data-model.md`, the constitution, or anything under `.specify/templates`, `.specify/scripts` or `.cursor/commands/speckit.*`. Merge by rebase. Record commit hashes against each item.

**Kyle, after merge:** install the Renovate GitHub App on `tomale-ai-ltd/tomale-rn-test` only.

---

## PR B: Expo SDK 58 and constitution 1.6.0 (`repo-sync/2026-11-0X-expo-58`)

Items: RS-2026-11-01-04 (Expo SDK 54 → 58), RS-2026-11-01-01 (constitution 1.6.0, folds in RS-2026-10-30-04). Needs PR A merged (Node 22.13+).

Prompt for Cursor:

> Apply RS-2026-11-01-04 then RS-2026-11-01-01.
> - Upgrade Expo one SDK at a time: 55, 56, 57, 58. For each: `npx expo install expo@^5X --fix`, read that SDK's release notes and apply the breaking changes, run `npx expo-doctor`, `pnpm typecheck`, `pnpm test`; one commit per SDK. Keep `newArchEnabled`. Let Expo pick React Native, Reanimated, worklets, expo-router, `@sentry/react-native` and `jest-expo` versions; don't hand-pin newer ones.
> - If an SDK step breaks something you can't fix cleanly, stop at the last green SDK and report.
> - Then run `/speckit.constitution` for 1.6.0 with a Sync Impact Report: Expo SDK 54 → 58; UI components NativeBase → gluestack-ui v5 with UniWind (Tailwind CSS v4); Lucide stays; `npm run` → `pnpm` in the schema procedure and gates, and in `package.json` scripts.
> Verify: `expo-doctor` clean; CI green. Kyle checks an EAS development build on iOS and Android: reaches Sign in, magic-link sign-in works, a Sentry test event arrives.

---

## PR C: build variants and UI library (`repo-sync/2026-11-0X-config`)

Items: RS-2026-10-30-07 (`app.config.js`), RS-2026-11-01-03 (gluestack-ui v5 + UniWind).

Production iOS bundle id and Android package: `ai.tomale.app` (Kyle, 01/11; registered in the Apple Developer account).

Prompt for Cursor:

> Apply RS-2026-10-30-07 and RS-2026-11-01-03.
> - Replace `app.json` with `app.config.js` driven by `APP_VARIANT`, set in each `eas.json` build profile: `development` → name "Tomale Dev", scheme `tomalerntest`, iOS bundle id and Android package `com.tomaleai.tomalerntest`; `preview` and `production` → name "Tomale", scheme `tomale`, bundle id / package `ai.tomale.app`. Default to `development` when `APP_VARIANT` is unset (local `expo start`). Keep every other `app.json` setting as it is (Sentry plugin, splash, icons, `web.output`, `newArchEnabled`). Keep `EXPO_PUBLIC_API_BASE_URL` per profile in `eas.json`.
> - Install gluestack-ui v5 (stable 5.x, not alpha) with UniWind and Tailwind CSS v4 per the official gluestack v5 UniWind guide; exact versions; no `nativewind` packages; wrap the root layout in `GluestackUIProvider`; add only Box, Text, Heading, Button, Input, Pressable, Image, Modal, Actionsheet under `components/ui/`. No restyling of existing screens.
> Verify: `pnpm typecheck`, `pnpm test`, the dev client starts to Sign in, `npx expo config --type public` shows the right scheme for `APP_VARIANT=development` and `production`, and a test Modal and Actionsheet open and animate on an iOS dev build.

---

## PR D: client session handling (speckit; becomes 007 automatically)

Implements [[use-expo-secure-store-for-client-tokens]] and [[use-axios-401-interceptor-for-client-auth-session-handling]] (constitution 1.5.0 rules), plus CTO #16 (Sentry user and profile context).

What the repo has today (read 01/11):
- `api/http.ts` is a **`fetch` wrapper, not Axios**. `axios` is installed but unused. Screens add `Authorization` headers by hand (`home/index.tsx`, `auth/complete.tsx`).
- `store/AuthStore.ts` persists `authToken` and `userId` to **AsyncStorage**. The **refresh token and `session_id` are never stored**, so no refresh is possible today.
- `app/auth/complete.tsx` accepts an **`authToken` straight from the deep-link URL**. Tokens must not arrive in URLs.
- `sentry.ts` strips `event.user.id`, so events can't be tied to a user.
- The `archive/003-foundations-state-backup` tag has a SecureStore helper worth reusing.

Scope:
1. **Storage.** Add `expo-secure-store` (`npx expo install`). Persist `authToken`, `refreshToken`, `userId`, `sessionId` and token issue time through a SecureStore-backed Zustand storage adapter (`AFTER_FIRST_UNLOCK`). Migrate once: read the legacy AsyncStorage `auth` key, write it to SecureStore and delete it. Capture `refreshToken` and `session_id` from `complete_magic_link`, `login` and `signup`. Web: fall back to memory only (no tokens in `localStorage`).
2. **HTTP client.** Rebuild `api/http.ts` on an Axios instance, keeping the current error shape (`err.response.{status,data}`, `err.normalized`) and adding the payload `code`. A request interceptor attaches the bearer token; remove the hand-written `Authorization` headers.
3. **401 interceptor** (constitution 1.5.0): on a 401 from a non-`/auth/*` request, one shared in-flight `POST /auth/refresh` (`users_id`, `refreshToken`), store the rotated tokens, retry the original request once. A 401 `invalid_refresh_token` → log out and go to Sign in. Network errors or 5xx on refresh → no logout; surface the error. On app foreground, refresh first if the token is older than 50 minutes (JWE, 1 h life, can't be decoded client-side).
4. **Deep link.** Remove the `authToken` URL-param path from `auth/complete.tsx`; only `token` → `complete_magic_link`. If any documented flow still sends `authToken`, stop and report instead.
5. **Sentry.** `Sentry.setUser({ id })` on sign-in, `null` on logout; tag `profile_id` when a profile is selected. `beforeSend` keeps `user.id` but strips email, username and IP.
6. **Tests (Jest):** concurrent 401s trigger one refresh; retry happens once; `/auth/*` is never retried; `invalid_refresh_token` logs out; a network error doesn't; legacy AsyncStorage tokens are migrated and deleted.

Don't change: Xano, `api/openapi`, `api/client.ts`, `data-model.md`, the auth screens' UX copy.
