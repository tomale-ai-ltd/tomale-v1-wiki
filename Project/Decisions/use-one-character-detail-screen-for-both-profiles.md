---
type: decision
title: "use-one-character-detail-screen-for-both-profiles"
project: tomale-rn-v1
status: accepted
date: "2026-11-12"
related:
  - "[[2026-11-12-001]]"
  - "[[008-characters-copy]]"
affects:
  - "[[PRD-Characters]]"
  - "specs/008-characters/spec.md"
features:
  - F-characters
---

# Decision: use-one-character-detail-screen-for-both-profiles

## What we decided
Kyle, 12/11 (008 clarify): one character detail screen serves both profiles. A grid tap or "See more" on the carousel panel opens it. The parent sees More (archive and delete); the child sees the same screen without More, and favourite and Draw again work there. The carousel panel stays short: actions plus up to 2 stories. Tapping the card again or the panel's Close control closes the panel; a swipe closes it and moves to the next character.

## Why
Not discussed in session notes.

## Alternatives considered
Not discussed in session notes.

## Trade-offs accepted
Not discussed in session notes.

## Workflow detail
After archive or delete, the parent stays on the list they were using and detail returns to the list that opened it. US3 checks the layout and the missing More control for a child; favourite is checked at US4 and Draw again at US5.

## Related notes
[[2026-11-12-001]], [[PRD-Characters]], [[008-characters-copy]]
