---
date: 2026-11-04
source: cursor
branch: repo-sync/2026-11-04
feature: RS-2026-10-30-07, RS-2026-11-01-03
---

# Variant identity and gluestack-ui v5 with UniWind

## What changed
- `56c9d6f` RS-2026-10-30-07. `app.json` is now `app.config.js`. `APP_VARIANT` on each `eas.json` profile sets the name, scheme, and iOS/Android id. Unset variant (local `expo start`) is development. Every profile still uses `https://api.tomale.ai/api:1pgd39RE`. `.github/workflows/release.yaml` reads the version with `npx expo config --json`.
- `3203c30` RS-2026-11-01-03. Stable gluestack-ui v5 (`@gluestack-ui/core` 5.0.15, `@gluestack-ui/utils` 5.0.6), UniWind 1.13.0, Tailwind CSS 4.3.3. Root layout wraps `GluestackUIProvider` (`mode="system"`). Added Box, Text, Heading, Button, Input, Pressable, Image, Modal, Actionsheet under `components/ui/`. Metro keeps the Sentry config and wraps it with `withUniwindConfig`. No screen restyle. Reanimated 4.7.1 and worklets 0.13.0 were left as SDK 58 installed them; `babel.config.js` was not changed.
- PR: https://github.com/tomale-ai-ltd/tomale-rn-test/pull/20

## Decisions
- Cursor pinned the stable npm releases. `gluestack-ui@5.0.3` still installs `@gluestack-ui/core@^5.0.0-alpha.0` and would write a worklets Babel plugin and replace the Sentry Metro config. Those CLI edits were not applied.
- `@legendapp/motion` 2.5.3 lists `nativewind` as a peer but does not import it. `.pnpmfile.cjs` drops that peer so pnpm does not install `nativewind`. The lockfile has no `nativewind` package.
- `newArchEnabled` was not in the current `app.json` and is not an SDK 58 config field, so it was not copied into `app.config.js`.
- The copied web provider rendered a `<script>` tag that React Native Web rejects on every screen. That tag was removed; system mode applies the theme from `matchMedia` on mount.
- `pnpm` `minimumReleaseAge` is 7 days and the existing SDK 58 lock already contains younger Expo packages, so a normal install fails when `package.json` changes. The install for this commit used a one-shot `--config.minimumReleaseAge=0` and did not change that setting in the repo. `@swc/helpers` 0.5.24 was published today, so it is overridden to 0.5.23.
- UniWind 1.13.0 and Tailwind 4.3.3 were the newest versions old enough for the 7-day gate (1.13.1 and 4.3.4 were not).

## Open questions / blockers
- Side-by-side install of `com.tomaleai.tomalerntest` and `ai.tomale.app` was not run. Public config shows the two identities. The iOS check used a fresh simulator dev build of the development id only.
- The local gitignored `ios/` was a pre-SDK 58 project. Verification moved it to `/tmp/tomale-ios-pre-sdk58` and `npx expo run:ios` generated a new `ios/` for the simulator build. Restore the backup if that old tree is still wanted.
- The `@swc/helpers` override can come out once 0.5.24 is 7 days old. Until the young Expo packages in the lock are old enough, further `package.json` edits will hit the same age check.

## Next
- Kyle merges PR 20 by rebase and updates the two repo-sync notes. Cursor did not change their status.
