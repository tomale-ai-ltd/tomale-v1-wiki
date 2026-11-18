---
date: 2026-11-18
source: cursor
branch: 009-profiles-pin
feature: 009-profiles-pin
---

# Profiles and PIN pull request opened

## What changed
- Pushed `009-profiles-pin` and opened https://github.com/tomale-ai-ltd/tomale-rn-test/pull/31 into main. Title: “009: profiles and PIN”. Not merged.
- The first `test` check failed: `.tests/main-auth-gate.test.tsx` imported the picker, which needs `EXPO_PUBLIC_API_BASE_URL`, and CI has no `.env`.
- `9b6e92c` Keep the main-route test off the profile screens. The rerun of `test` passed: https://github.com/tomale-ai-ltd/tomale-rn-test/actions/runs/44395257982/job/135123336706

## Decisions
- Kyle asked for the PR after the phone pass, with US1–US5, the listed phone-pass commits, RS-2026-11-17-03, RS-2026-11-18-01, and snags S-006 to S-018 left out. Cursor added the test fix so the required check could pass.

## Open questions / blockers
- Kyle merges. Cursor did not.

## Next
- Kyle's review of PR 31.
