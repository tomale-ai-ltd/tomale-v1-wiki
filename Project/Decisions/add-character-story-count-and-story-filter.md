---
type: decision
title: "add-character-story-count-and-story-filter"
project: tomale-rn-v1
status: accepted
date: "2026-11-06"
related:
  - "[[2026-11-06-002]]"
  - "[[share-characters-across-the-household]]"
  - "[[per-child-story-visibility]]"
affects:
  - "[[PRD-Characters]]"
  - "characters"
  - "instant_stories"
features:
  - F-characters
---

# Decision: add-character-story-count-and-story-filter

## What we decided

Before speckit 008 (Characters), add the backend pieces the screen needs (Kyle, 06/11: "add them"):
- `GET /characters` returns `created_at` and `stories_count` per character.
- `GET /instant_stories` takes an optional `characters_id` filter ("stories with this character"); it inherits per-child story visibility.
- `GET /characters/{id}` returns a trimmed detail output instead of the raw record.

The split above is the proposal from the session; a Xano brief and Postman tests follow.

## Why

008 prep found gaps: the list has no story count or created date, there is no "stories with this character" endpoint, and the detail endpoint returns the raw record.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes. Open: whether a child's `stories_count` covers all family stories or only the child's own (Claude suggested their own, to match the story list).

## Workflow detail

Xano brief for the additions, then Postman tests; then Characters mock-up round 2 and `/speckit.specify` for 008. The OpenAPI and data model regen follows the Xano publish through repo-sync.

## Related notes

[[2026-11-06-002]], [[PRD-Characters]], [[share-characters-across-the-household]], [[per-child-story-visibility]]
