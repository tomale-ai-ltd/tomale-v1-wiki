---
date: 2026-11-03
source: cursor
branch: repo-sync/2026-11-03-expo-58
feature: RS-2026-11-01-04, RS-2026-11-01-01, RS-2026-11-01-06
---

# PR B Expo SDK 58 and constitution 1.6.0

## What changed
- Opened PR #19: https://github.com/tomale-ai-ltd/tomale-rn-test/pull/19.
- Applied RS-2026-11-01-04 as four SDK commits:
  - `500ef52` RS-2026-11-01-04 Upgrade Expo SDK 54 to 55
  - `db795e0` RS-2026-11-01-04 Upgrade Expo SDK 55 to 56
  - `017b1a0` RS-2026-11-01-04 Upgrade Expo SDK 56 to 57
  - `bd5ba1e` RS-2026-11-01-04 Upgrade Expo SDK 57 to 58
- Applied RS-2026-11-01-01:
  - `fcb2fdd` RS-2026-11-01-01 Amend constitution to 1.6.0
- Applied RS-2026-11-01-06:
  - `157be7e` RS-2026-11-01-06 Remove one-off audit exceptions
- CI `test` check is green on PR #19.

## Decisions
- Kyle approved committing SDK 56 with an Expo Doctor exception because only the known Hermes v1 regression remained; the commit message links the SDK 57 changelog entry and SDK 57/58 doctor checks are green.
- Cursor kept the five node-forge GHSA ignores because Expo SDK 58 CLI still resolves `node-forge@1.4.0`; removing them makes `pnpm audit --audit-level=high` fail.
- Cursor force-pushed with lease after folding SDK 58 lint fixes into the SDK 58 commit to keep one commit per item.

## Open questions / blockers
- Kyle still needs to verify an EAS iOS development build reaches Sign in, magic-link sign-in works, and a Sentry test event arrives.

## Next
- Kyle reviews and merges PR #19 when ready.
