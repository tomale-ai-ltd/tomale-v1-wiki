---
date: 2026-10-30
source: cursor
branch: repo-sync/2026-10-29, repo-sync/2026-10-29-pnpm
feature: B10 repo sync
---

# B10 repo sync landed on wip as PR #11 and PR #12

## What changed
- [PR #11](https://github.com/tomale-ai-ltd/tomale-rn-test/pull/11) merged 2026-10-29 onto `wip/pre-restructure-2026-10-24`: constitution 1.5.0, specify-rules cleanup, sed escape, optional micro-PRD, Cursor rules and ignores, EAS and `.env.example` API URL, data-model catalogues. Follow-up commit hid the template note and split the steps heading.
- [PR #12](https://github.com/tomale-ai-ltd/tomale-rn-test/pull/12) merged 2026-10-30: pnpm 10.34.7, constitution 1.5.1, `pnpm-lock.yaml` replaces `package-lock.json`, axios 1.20.0, hoisted linker after Jest failed on the isolated layout, `web.output` `single` so a browser-like Metro request does not server-render AuthStore, typecheck fixes (`readonly string[]`, `globalThis`), and a small same-major audit override set. Direct dependency versions match the npm lock except axios.

## Decisions
- Kyle approved pnpm 10 (not 11), a 7-day `minimumReleaseAge`, and build scripts only for `@sentry/cli` and `unrs-resolver`.
- Kyle approved same-major overrides for highs, and `ignoreGhsas` when the fix is a major bump under Expo, Metro, or Jest, or when there is no patch. Runtime packages are not accepted.
- Kyle rejected the `decode-uri-component` 0.2 → 0.5 override: 0.5.1 is ESM-only and `query-string` 7 is CommonJS. The high stays ignored; the lockfile stays on 0.2.2.
- Cursor set `node-linker=hoisted` because Jest could not transform `react-native/jest/setup.js` under `node_modules/.pnpm`.
- Cursor pinned `lint-staged`, `prettier`, and `yaml` to the npm-lock versions after a fresh resolve floated those ranges.

## Open questions / blockers
- No EAS build has been seen to confirm Expo picks pnpm from `pnpm-lock.yaml` alone.
- `GHSA-qr28-fpjm-wq7f` on `decode-uri-component` should be revisited when expo-router no longer depends on `query-string` 7.
- The AuthStore `window is not defined` crash still happens if something server-renders the app. `web.output` `single` only stops that path for browser-like Metro requests.

## Next
- B10 is on wip. Nothing else is open on these two PRs.
