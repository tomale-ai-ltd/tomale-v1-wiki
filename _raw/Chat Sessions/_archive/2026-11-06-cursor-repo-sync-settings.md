---
date: 2026-11-06
source: cursor
branch: repo-sync/2026-11-06
feature: RS-2026-11-05-05
---

# Settings opens from the parent avatar

## What changed
- Fix-up `528b7c2ef3c1036bd5cdd825721cc49c788d499f` on PR https://github.com/tomale-ai-ltd/tomale-rn-test/pull/23. Not merged. The earlier RS-2026-11-05-05 commit was already pushed, so this is a new commit.
- Parent tabs are Home, Create, Bookshelf, Characters, and Store. Child tabs are Home, Create, Bookshelf, and Characters. Settings is not a tab. A parent opens it from the header avatar. A child who opens the Settings route is sent to Home.
- Local lint, typecheck, and Jest passed. GitHub `test` passed in 1m7s (`gh pr checks`).

## Decisions
- Kyle (06/11): follow RS-2026-11-05-05 and the decision note as written. The earlier correction that kept Settings as a parent tab is withdrawn.

## Open questions / blockers
- `GET /auth/me` still types `auth` as a string and does not declare `active_profile`.

## Next
- Kyle reviews PR #23. Cursor does not merge.
