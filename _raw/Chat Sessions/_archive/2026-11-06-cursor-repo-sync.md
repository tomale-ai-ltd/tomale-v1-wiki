---
date: 2026-11-06
source: cursor
branch: repo-sync/2026-11-06
feature: repo-sync/2026-11-06
---

# Repo-sync batch for 6 November

## What changed
- PR https://github.com/tomale-ai-ltd/tomale-rn-test/pull/23 on `repo-sync/2026-11-06`. Not merged. GitHub `test` passed in 1m20s on the PR head (`gh pr checks`).
- `1ba25437f1cb1cf4f4fda8ce09d3170cb87ab483` RS-2026-11-05-04 regenerate OpenAPI and the data model.
- `5d1f48271fea2df7f41a5e438443803e7d849c64` RS-2026-11-05-02 constitution 1.6.1.
- `f6b58b4799256d0e62e084c89cf21444e16f3e9f` RS-2026-11-05-03 remove the Home OTA marker.
- `f2abb8dc4df7e80c76df8731b5c02d4a5f963a99` RS-2026-11-04-04 CI `test` check rule.
- `036ca7f84422441e9d587b54ec76abe48dcc19b5` RS-2026-11-06-01 contract fixtures rule.
- `af49690e1132de47676230e093924aae5885e276` RS-2026-11-05-01 design-system theme, Glacial Indifference, brand icons.
- `8c0c471330e9fcab219e33edcd121a7004050e26` RS-2026-11-05-05 profile-aware tabs.
- `59a3278f585313f5c61c499018331f16771267b7` PU-2026-11-04-01 align `tomale-api.mdc` with constitution 1.6.1.
- RS-2026-11-05-06 was not in this batch.

## Decisions
- Kyle (06/11): the Settings tab stays visible for a parent profile and is hidden for a child profile. The approved item and [[use-profile-aware-bottom-tabs-with-home-dashboard]] say Settings leaves the tab bar and sits behind the avatar (parent only). This batch follows Kyle's correction.
- Cursor did not hand-edit `api/openapi/xano.yaml`. Regenerated `GET /auth/me` types `auth` as a string and does not declare `active_profile`.

## Open questions / blockers
- Backend: `GET /auth/me` still needs an explicit response shape for `auth.active_profile` (`id` string UUID, `name`, `is_child`).
- Dev build not checked here for Glacial Indifference or light/dark screens. Tab sets are covered by Jest, not by a profile switch on a device.

## Next
- Kyle reviews PR #23. Cursor does not merge.
