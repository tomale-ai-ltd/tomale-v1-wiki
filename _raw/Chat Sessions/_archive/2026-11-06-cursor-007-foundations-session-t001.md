---
date: 2026-11-06
source: cursor
branch: 007-foundations-session
feature: 007-foundations-session
---

# T001 secure-store install, not committed

## What changed
- Pulled `007-foundations-session`; already at `489b0b2`.
- Kyle approved all 33 locked versions younger than 7 days. Added them to `minimumReleaseAgeExclude` under the temporary RS-2026-11-05-06 comment. `minimumReleaseAge` and the existing security excludes were left as they were.
- `npx expo install expo-secure-store` resolved `expo-secure-store@58.0.2` (`~58.0.2` in package.json). No other package was added or upgraded. The lockfile also dropped `bufferutil` and `utf-8-validate` from the transitive peer list of `@react-native/metro-config@0.88.1`. Not committed. Expo could not write the config plugin into `app.config.js`.

## Decisions
- Kyle approved the full 33-version exclude list, including `react-native-safe-area-context@5.11.1` and the modules-macros builds.

## Open questions / blockers
- T026 device checks wait on the iOS development build `dc1b2f3b-2621-4949-a4bc-4ebf201b1777`.

## Next
- Install that build and run the quickstart device checks. Do not open a PR.

## Follow-up
- Kyle asked to pin `expo-secure-store` to exact `58.0.2`, add the config plugin with `configureAndroidBackup: true` and `faceIDPermission: false`, then commit T001. Those option names match the installed 58.0.2 plugin types. `npx expo config --type prebuild` exited 0. Lint, typecheck, and 25 tests passed. Commit `046487e`. Not pushed.
- T014–T016: `store/secureSessionStorage.ts` chunks values over 2000 characters into `auth`, `auth.1`, … with `AFTER_FIRST_UNLOCK`. Web uses an in-memory map. A legacy AsyncStorage `auth` value is copied once and deleted. An unreadable payload is deleted and returns null. A locked keychain error retries when the app becomes active or with backoff from 500 ms to 5 s, and does not clear the session. A missing `tomale.installed` flag drops leftover keychain chunks after a legacy migration check, so a reinstall starts signed out and an upgrade still migrates. Commit `ff95f6a`. Pushed with `046487e`. No PR.
- T021 sets the Sentry account id and `profile_id` tag from `applySession` and rehydration, and clears the tag when the profile id is null. T024 found no remaining hand-written Authorization headers in `app/` or `hooks/`. T025: the session, secure-storage, and Sentry Jest files passed, and `pnpm check` passed. Commit `6578a9f`. Pushed. No PR.
- Kyle asked for `eas build --profile development --platform ios`. Build `dc1b2f3b-2621-4949-a4bc-4ebf201b1777` for `com.tomaleai.tomalerntest` finished successfully.
- T026 Sentry trigger: `debug/devGlobals.ts` registers dev-menu item "Send Sentry test error", which calls `Sentry.captureException(new Error("007 test"))`. Local `.env` has a real `EXPO_PUBLIC_SENTRY_DSN`. `sentry.ts` does not set `enabled: false`. SDK 8.28.0 still sends while `__DEV__` is true.
- T026 device results: checks 1, 2, and 5 passed. Check 3 marked not applicable because no released build stores the session in AsyncStorage. Fixes in `2f7c9ae`: profile tag is set only as a non-empty string and removed when empty (REACT-NATIVE-7 had `profile_id` `<invalid>`); the dev menu item is skipped on web; a hydrated signed-out `(main)` route redirects to sign-in. Pushed. No PR. Kyle will re-run the Sentry check.
- Kyle found `GET /auth/me` returns `{ user, auth: { active_profile: { id, name, is_child } } }`. `readActiveProfileId` now reads `auth.active_profile.id`. The old top-level shape returns null. Commit `1707a5f`. Pushed. No PR.
- Kyle confirmed the Sentry check passes. T026 recorded in `checklists/validation.md` and ticked. PR D is https://github.com/tomale-ai-ltd/tomale-rn-test/pull/22. CI `test` passed. Not merged.
