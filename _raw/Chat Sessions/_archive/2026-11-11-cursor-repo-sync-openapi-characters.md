---
date: 2026-11-11
source: cursor
branch: repo-sync/2026-11-11b
feature: RS-2026-11-11-01
---

# OpenAPI regen did not include the Characters response fields

## What changed
- Branched `repo-sync/2026-11-11b` from `main` and ran `pnpm update:openapi && pnpm update:datamodel`. No commit and no PR. The generated files were restored.
- `GET /instant_stories` gained optional query `characters_id` (int64). `instant_story_characters` gained btree indexes on `characters_id` and `instant_stories_id`. The table's `id` default came back as `0`.
- `GET /characters` changed from an array of 9 fields to `{ type: object, properties: {} }`. `GET /characters/{characters_id}` changed from 18 fields to the same empty object. `stories_count` does not appear in `api/openapi/xano.yaml`.

## Decisions
- Kyle asked for generated files only, then a check that the list has `created_at` and `stories_count`, the detail has the 12 fields, and the story list has `characters_id`.
- Cursor did not commit. The detail and list checks failed, and committing would drop the fields already in the contract.

## Open questions / blockers
- The live Xano OpenAPI export has no response properties for those two character GETs. The 12 detail fields are `id`, `name`, `status`, `is_deleted`, `instant_stories_id`, `last_modified_at`, `deleted_at`, `is_favourite`, `cover_image`, `created_at`, `physical_description`, `stories_count`.

## Next
- Republish or fix the Xano OpenAPI output for `GET /characters` and `GET /characters/{characters_id}`, then rerun RS-2026-11-11-01.
