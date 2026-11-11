---
type: brief
title: characters-008-additions-brief
project: tomale-rn-v1
status: done
date: 2026-11-10
related:
  - "[[PRD-Characters]]"
  - "[[add-character-story-count-and-story-filter]]"
  - "[[per-child-story-visibility]]"
  - "[[backend-xano]]"
---

# Characters additions before speckit 008: Xano brief

From [[add-character-story-count-and-story-filter]] (Kyle, 06/11) and PU-2026-11-10-01. Checked against the mirror at `c167fea` (06/11). Same process as [[characters-backend-prep-brief]]: Xano AI drafts → Claude reviews against the mirror → Kyle publishes → Postman folder 5.

**Decided 10/11 (Kyle):** a child's story count covers only the stories that child can see, so it always matches the "Stories with [name]" list.

## Visibility rule (must match `GET /instant_stories` exactly)
A story is visible when `users_id == $auth.id`, `is_deleted != true`, and either the active profile is a parent (`is_child == false`), or the story's `user_profiles_id` is the active profile's id and (`status_moderation == "Pass"` or (`status_moderation == "Parental Approval"` and `parent_approved`)). Fail closed: a missing `active_profile` counts as a child with no stories.

## Change set 1: a shared visibility function
New function `stories/visible_story_ids`, inputs `int users_id`, `uuid? active_profile_id`, `bool? is_child`. Returns the list of story ids visible under the rule above (query `instant stories`, output `id` only). Treat `is_child` null as true (fail closed). Callers pass `$auth.id` and the values from `$auth.extras.active_profile`.
- Leave the `where` in `GET /instant_stories` as it is for now (it's tested); note in a comment that it must stay identical to this function.

## Change set 2: index the join table
`instant_story_characters`: add btree indexes on `characters_id` and on `instant_stories_id`. Index only; no schema or data change.

## Change set 3: `GET /characters` adds `created_at` and `stories_count`
- Add `created_at` to the output list (keep the existing 9 fields, nothing else).
- Add `stories_count` (int) per character: the number of distinct visible stories (change set 1) linked to that character in `instant_story_characters`. Do it with one query for the visible ids and one for the links (`characters_id in` this page's ids and `instant_stories_id in` the visible ids), then count per character. No per-row queries in a loop.
- Characters with no visible stories get `0`.

## Change set 4: `GET /characters/{characters_id}` returns a trimmed detail
Today it returns the raw record (internal fields included). Return exactly: the 10 list fields above, `physical_description`, and `stories_count` (same rule). Ownership and not-deleted checks unchanged (404 otherwise). Archived characters: a parent may open one; a child gets 404 (same fail-closed parent check as the list).

## Change set 5: `GET /instant_stories` filter by character
Add optional input `int? characters_id?`. When given, return only stories linked to that character in `instant_story_characters`, on top of every existing filter and the visibility rule (so a child sees only their own, approved stories). Look up the linked story ids first, then add `$db.instant_stories.id in <ids>` to the existing `where`. A character id from another account simply returns an empty list (stories are already owner-filtered); no error. Change nothing else in the endpoint.

## Conventions
Explicit inputs, `$auth.id` for ownership, no `enforce_hidden_fields = false` on these reads, error text without status numbers. Publish one change set at a time, in order.

## Postman (`_tests` folder 5 additions, after publishing)
- 5H: link the test character to the Draft story (5C-2 does this) → `GET /characters` shows that character with `stories_count` ≥ 1 and a numeric `created_at`.
- 5I: `GET /characters/{id}` returns only the 12 fields; no `users_id`, attributes or `data_models_id`.
- 5J: `GET /instant_stories?characters_id={{charTestId}}` returns the linked story and only stories linked to it.
- 5K (child, after 5E-0): `GET /characters` `stories_count` for the test character counts only the child's visible stories (0 for the Draft story created by the parent); `GET /instant_stories?characters_id=` returns none of the parent's stories.
- 5L (user2): `GET /instant_stories?characters_id={{charTestId}}` returns an empty list; `GET /characters/{id}` 404.
