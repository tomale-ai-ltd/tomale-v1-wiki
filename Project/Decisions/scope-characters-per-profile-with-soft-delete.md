---
type: decision
title: scope-characters-per-profile-with-soft-delete
project: tomale-rn-v1
status: superseded
date: 2026-10-28
related:
  - "[[v1-audit]]"
  - "[[per-child-story-visibility]]"
affects:
  - characters
  - characters endpoints
  - PRD-Characters
features:
  - F-characters
  - F-profiles
superseded_by: "[[share-characters-across-the-household]]"
---

# Decision: scope-characters-per-profile-with-soft-delete

## What we decided

For Slice 100 (feature 007):

- Characters belong to a **profile**, like stories: add `user_profiles_id`, backfill existing rows, and scope the endpoints the same way as `instant_stories`.
- **Soft delete only**, via `deleted_at`. The overlapping `status` (active/archived) and `is_deleted` fields go.
- **No PATCH in V1** for now: edits would need the name-moderation check. Whether "Edit character" and "Re-create image" (MVP in the umbrella PRD) become delete-and-recreate or a later moderated PATCH is decided in B9.
- Names are moderated on create by the existing custom function ([[moderate-names-in-two-stages]]).
- `characters.instant_stories_id` is no longer meaningful and is dropped (`instant_story_characters` links characters to stories).

These are backend changes in Xano to make before the 007 frontend work.

## Why

Simplicity, and consistency with per-child story visibility.

## Trade-offs accepted

Household members can't share characters in V1.


**Amendment (2026-10-29, B9 review with Kyle):**
- `user_profiles_id` is nullable: `null` means household-wide, so a parent can create a character for themselves, a child, or everyone. Single value, no array.
- `status`, `is_deleted` and `deleted_at` are kept as built (archive plus soft delete).
- `instant_stories_id` is kept as "created in", but story links use the many-to-many `instant_story_characters`. Existing characters join a story through a new `POST /instant_stories/{id}/characters`.
- Re-create image (image-to-image) and favourites are added; text edit stays out of V1.

See [[PRD-Characters]].

## Related notes

- [[v1-audit]] (§7)
- [[per-child-story-visibility]]
