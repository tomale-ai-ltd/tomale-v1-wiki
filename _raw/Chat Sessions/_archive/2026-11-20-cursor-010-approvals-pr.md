---
date: 2026-11-20
source: cursor
branch: 010-approvals
feature: 010-approvals
---

# Opened PR 32 for 010 approvals

## What changed
- Pushed `010-approvals` and opened https://github.com/tomale-ai-ltd/tomale-rn-test/pull/32 into `main`, titled “010: approvals”. Not merged.
- GitHub `test` passed in 1m19s: https://github.com/tomale-ai-ltd/tomale-rn-test/actions/runs/44646432844/job/135990084412
- Description covers US1–US5, B6 `user_profiles_id` and nullable pictures, pre-merge fixes including `e5b8c76`, `e93b2d8`, `8db3f41` through `3dac4eb`, `31a5bba`, `9a36c1e`, `0cbab5f`, `5db1238`, and `89ddcec`. Snags S-019 to S-022 left for the vault. Failed-keep stays on `decide.keep` unit tests.

## Decisions
- Cursor included `31a5bba` in the PR description because it sits on the branch between the phone-pass range and `9a36c1e`. Kyle’s list did not name it.

## Open questions / blockers
- Kyle still needs to retest the signed-out approvals link after `89ddcec` (one PIN, inbox stays, Back goes to Home). Settings already passed.

## Next
- Kyle reviews PR 32. Do not merge from this session.
