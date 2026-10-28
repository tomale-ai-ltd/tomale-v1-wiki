---
type: decision
title: scope-characters-per-profile-with-soft-delete
project: tomale-rn-v1
status: accepted
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

## Related notes

- [[v1-audit]] (§7)
- [[per-child-story-visibility]]
