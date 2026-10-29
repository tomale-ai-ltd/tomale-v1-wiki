---
type: decision
title: share-characters-across-the-household
project: tomale-rn-v1
status: accepted
date: 2026-10-29
supersedes:
  - "[[scope-characters-per-profile-with-soft-delete]]"
related:
  - "[[PRD-Characters]]"
  - "[[moderate-names-in-two-stages]]"
affects:
  - characters
  - "[[PRD-Characters]]"
features:
  - F-characters
  - F-profiles
---

# Decision: share-characters-across-the-household

## What we decided

For Slice 100 (speckit 007), replacing the per-profile approach decided on 28/10:

- **Characters are visible to every profile in the household.** They stay account-scoped (`users_id`), as built; no per-profile ownership column.
- **Only parent profiles can delete or archive** a character. The check uses the active profile's `is_child`.
- **Archive and soft delete are both kept** as built (`status`, `is_deleted`, `deleted_at`).
- **Stories link characters through `instant_story_characters`** (many-to-many). Existing characters join a story through a new `POST /instant_stories/{id}/characters`. `characters.instant_stories_id` stays as "created in".
- **No text edit in V1.** Visual changes go through "re-create image" (image-to-image, entitlement-gated). There's a small endpoint for `status` and `is_favourite` only.
- **Names and descriptions are moderated on create**, with a generic message on failure ([[moderate-names-in-two-stages]]).

## Why

Kyle (29/10): per-profile visibility was overthinking it. Characters are shared family creations, and moderation already covers names and descriptions. It also removes a schema change and the backfill. Restricting deletion to parents protects shared characters while it's unclear how independently young children will use the app.

## Alternatives considered

- Per-profile ownership (the 28/10 decision).
- Nullable owner with household-wide `null` (proposed in the B9 review).

## Trade-offs accepted

A child can see characters other household members made. Stories stay per-profile ([[per-child-story-visibility]]).

## Related notes

- [[PRD-Characters]]
- [[v1-audit]]
