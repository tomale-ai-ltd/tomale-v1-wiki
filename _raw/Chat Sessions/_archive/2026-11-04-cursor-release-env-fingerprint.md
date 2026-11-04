---
date: 2026-11-04
source: cursor
branch: repo-sync/2026-11-04
feature: RS-2026-11-04-02, RS-2026-10-30-07
---

# Release startup crash and fingerprint runtime version

## What changed
- Root cause of the preview Release crash: `config/env.ts` read `process.env[name]`. babel-preset-expo only inlines a static `process.env.EXPO_PUBLIC_*` member, so the Release bundle threw `[env] Missing required environment variable: EXPO_PUBLIC_API_BASE_URL` during startup. expo-updates then aborted on `expo.controller.errorRecoveryQueue` (SIGABRT). Reproduced on the simulator Release build before the fix.
- `4ebcdee` RS-2026-11-04-02. `config/env.ts` now reads `process.env.EXPO_PUBLIC_API_BASE_URL` directly. No other dynamic `process.env[` read in app TypeScript. `sentry.ts` was already static. The Node scripts `scripts/check-env.mjs`, `scripts/update-openapi.mjs`, and `scripts/update-data-model.mjs` still use dynamic reads; they run in Node, not in the app bundle.
- `536aea4` RS-2026-10-30-07, rewritten. `runtimeVersion` policy is `fingerprint` instead of `appVersion`.
- `c583b48` is the rebased gluestack commit. Pushed with `--force-with-lease` to https://github.com/tomale-ai-ltd/tomale-rn-test/pull/20. Not merged.
- After the fix, the simulator Release build stayed up on Sign in.

## Decisions
- Kyle asked for the env fix as its own commit and the fingerprint change inside the existing variant commit. Cursor rewrote that commit and force-pushed the feature branch with `--force-with-lease`.

## Open questions / blockers
- `eas update:list` on branch `production` (the channel the preview profile points at) has five update groups, all runtime version `1.0.0`, newest first: "OTA update - validate OTA works in preview builds", "Enable OTA check in dev mode for validation", "Final OTA Validation - visible marker test", "observability test #2", "observability test". All about 11 months old, by tomale-ai. No other branches have updates. A fingerprint runtime version will not match `1.0.0`, so those updates will not install on an SDK 58 build. The next EAS build has to be a native build so the embedded runtime version is the fingerprint; an OTA cannot change it.
- The local `ios/` project used for the Release check is still the development prebuild (`TomaleDev`, `com.tomaleai.tomalerntest`). The crash and the Sign in check were the Release JavaScript bundle. Sentry source-map upload was disabled for that local build because this machine has no Sentry auth token.

## Next
- Kyle merges PR 20 by rebase and updates the repo-sync notes. Cursor did not change their status.
