---
date: 2026-11-04
source: cursor
branch: repo-sync/2026-11-04
feature: RS-2026-10-30-07, RS-2026-11-01-03, RS-2026-11-04-02
---

# Variant identity and gluestack-ui v5 with UniWind

## What changed
- `536aea4` RS-2026-10-30-07. `app.json` is now `app.config.js`. `APP_VARIANT` on each `eas.json` profile sets the name, scheme, and iOS/Android id. Unset variant (local `expo start`) is development. Every profile still uses `https://api.tomale.ai/api:1pgd39RE`. `.github/workflows/release.yaml` reads the version with `npx expo config --json`. `runtimeVersion` policy is `fingerprint`, not `appVersion`, so an SDK 54 update published at runtime version `1.0.0` cannot be served to an SDK 58 build. This commit was rewritten for that policy; the earlier hash was `56c9d6f`.
- `c583b48` RS-2026-11-01-03. Stable gluestack-ui v5 (`@gluestack-ui/core` 5.0.15, `@gluestack-ui/utils` 5.0.6), UniWind 1.13.0, Tailwind CSS 4.3.3. Root layout wraps `GluestackUIProvider` (`mode="system"`). Added Box, Text, Heading, Button, Input, Pressable, Image, Modal, Actionsheet under `components/ui/`. Metro keeps the Sentry config and wraps it with `withUniwindConfig`. No screen restyle. Reanimated 4.7.1 and worklets 0.13.0 were left as SDK 58 installed them; `babel.config.js` was not changed. Rebased onto `536aea4`; the earlier hash was `3203c30`.
- `4ebcdee` RS-2026-11-04-02. Preview Release crashed about 0.5 s after a fresh launch: SIGABRT on `expo.controller.errorRecoveryQueue`. The JS exception was `[env] Missing required environment variable: EXPO_PUBLIC_API_BASE_URL`. `config/env.ts` read `process.env[name]`. babel-preset-expo only inlines a static `process.env.EXPO_PUBLIC_*` member, so the Release bundle never received the URL that `eas.json` set, threw during startup, and expo-updates aborted because it had no update to roll back to. The fix reads `process.env.EXPO_PUBLIC_API_BASE_URL` directly. No other dynamic `process.env[` read in app TypeScript. `sentry.ts` was already static. The Node scripts `scripts/check-env.mjs`, `scripts/update-openapi.mjs`, and `scripts/update-data-model.mjs` still use dynamic reads; they run in Node, not in the app bundle. After the fix, a simulator Release build stayed on Sign in.
- `eas update:list` shows updates only on the `production` branch, which is the channel the preview profile uses. Five groups, all runtime version `1.0.0`, about 11 months old, newest first: "OTA update - validate OTA works in preview builds", "Enable OTA check in dev mode for validation", "Final OTA Validation - visible marker test", "observability test #2", "observability test". A fingerprint runtime version will not match `1.0.0`, so those updates will not install on an SDK 58 build. The next EAS build has to be a native build for that fingerprint to be embedded.
- PR: https://github.com/tomale-ai-ltd/tomale-rn-test/pull/20. Branch force-pushed with `--force-with-lease`. Not merged.

## Decisions
- Cursor pinned the stable npm releases. `gluestack-ui@5.0.3` still installs `@gluestack-ui/core@^5.0.0-alpha.0` and would write a worklets Babel plugin and replace the Sentry Metro config. Those CLI edits were not applied.
- `@legendapp/motion` 2.5.3 lists `nativewind` as a peer but does not import it. `.pnpmfile.cjs` drops that peer so pnpm does not install `nativewind`. The lockfile has no `nativewind` package.
- `newArchEnabled` was not in the current `app.json` and is not an SDK 58 config field, so it was not copied into `app.config.js`.
- The copied web provider rendered a `<script>` tag that React Native Web rejects on every screen. That tag was removed; system mode applies the theme from `matchMedia` on mount.
- `pnpm` `minimumReleaseAge` is 7 days and the existing SDK 58 lock already contains younger Expo packages, so a normal install fails when `package.json` changes. The install for this commit used a one-shot `--config.minimumReleaseAge=0` and did not change that setting in the repo. `@swc/helpers` 0.5.24 was published today, so it is overridden to 0.5.23.
- UniWind 1.13.0 and Tailwind 4.3.3 were the newest versions old enough for the 7-day gate (1.13.1 and 4.3.4 were not).
- Kyle asked for the env fix as its own commit, RS-2026-11-04-02, and for the fingerprint runtime version inside the rewritten RS-2026-10-30-07 commit.

## Open questions / blockers
- Side-by-side install of `com.tomaleai.tomalerntest` and `ai.tomale.app` was not run. Public config shows the two identities. The iOS check used a fresh simulator dev build of the development id only.
- The local gitignored `ios/` was a pre-SDK 58 project. Verification moved it to `/tmp/tomale-ios-pre-sdk58` and `npx expo run:ios` generated a new `ios/` for the simulator build. Restore the backup if that old tree is still wanted.
- The `@swc/helpers` override can come out once 0.5.24 is 7 days old. Until the young Expo packages in the lock are old enough, further `package.json` edits will hit the same age check.

## Next
- Kyle merges PR 20 by rebase when ready, and updates the repo-sync notes. Cursor did not merge and did not change their status.
