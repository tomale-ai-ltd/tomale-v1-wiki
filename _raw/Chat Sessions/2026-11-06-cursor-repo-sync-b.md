---
date: 2026-11-06
source: cursor
branch: repo-sync/2026-11-06b
feature: RS-2026-11-06-03, RS-2026-11-06-02
---

# Repo sync 2026-11-06b: OpenAPI regen and auth/logout

## What changed
- Branch `repo-sync/2026-11-06b` from main. PR https://github.com/tomale-ai-ltd/tomale-rn-test/pull/24. Not merged.
- `f873f4d7f5fb1d975d6ee8728e42e053c0e999dd` RS-2026-11-06-03: regenerate OpenAPI and the data model. `POST /auth/logout` is in the contract. User sessions can be `revoked`. `GET /auth/me` still types `auth` as a string and does not declare `auth.active_profile`, so `readActiveProfileId` and the `/auth/me` fixtures were left as they are.
- `2481a48c0746f0f3a32ceda6b73aac81e4cc1c60` RS-2026-11-06-02: a user-initiated sign-out calls `POST /auth/logout` with the stored `session_id` before clearing the local session. Skipped when no session id is stored. A network error, a 401, or any other failure still clears the local session. A rejected refresh does not call logout. Numeric stored ids are sent as integers.
- Local lint, typecheck, and Jest (8 suites, 47 tests) passed. GitHub `test` passed in 1m10s (run 42226323554, job 127920629537).

## Decisions
- Kyle asked for this batch: one branch, one commit per item, one PR, wait for `test`, do not merge.
- Cursor left the profile readers on the unknown-shape parser because the regenerated spec still types `auth` as a string. No hand edit of the spec or data model.

## Open questions / blockers
- Xano's export still does not declare `auth.active_profile`. Backend needs an explicit response shape before the app can switch to the generated type.
- Device check not run: sign out, then reuse the old refresh token in Postman and expect 401 `invalid_refresh_token`.

## Next
- Kyle reviews and merges PR #24. Cursor does not update the repo-sync item status.
