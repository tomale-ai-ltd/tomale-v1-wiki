---
date: 2026-11-24
source: cursor
branch: 010b-auth-signup
feature: 010b-auth-signup
---

# Phone follow-up: rename name + Set PIN cold start

## What changed
- `4a08143` — `useActiveProfile` overlays `profilesStore` name (and header prefers list match) so Home / greeting update after rename without refetching `/auth/me`.
- `ab93df3` — Name step reseeds when `primary.id` changes (not a one-shot boolean), so a new session does not keep a prior seed.
- `43bcbfe` — `noteIntentionalSetPin` / `takeIntentionalSetPin`; picker treats primary as already-here while `/auth/me` is null; cold-start restored set-pin redirects home unless intentional; call sites: picker, manage (add / Change PIN), edit `PIN_NOT_SET`, magic-link unlock.
- `3328d4c` — Face ID still wiping Sign in: draft is the live field source; `clearSessionCaches` no longer clears it; signed-out `refreshSession` does not `replace` onto Sign in; root stack stays mounted after first paint; email uses `username` autofill type.
- Typecheck clean; related jest suites passed. Not pushed.

## Decisions
- Kyle approved the three-fix order (header → Name seed → Set PIN) before coding.
- Cursor chose a module flag for intentional Set PIN (clears on JS cold start) over persisting route intent.
- Kyle reported Face ID autofill still remounting/wiping after `9da97a6`; Cursor hardened remount paths rather than only storing a draft copy.

## Open questions / blockers
- None.

## Next
- PR #34 open into main (CI `test` green). Do not merge until Kyle re-passes Face ID autofill + rename / Set PIN / Name seed after the follow-up commits.
