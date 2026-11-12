---
type: decision
title: "make-character-favourite-and-archive-optimistic"
project: tomale-rn-v1
status: accepted
date: "2026-11-12"
related:
  - "[[2026-11-12-001]]"
affects:
  - "specs/008-characters/plan.md"
  - "specs/008-characters/spec.md"
features:
  - F-characters
---

# Decision: make-character-favourite-and-archive-optimistic

## What we decided
Kyle, 12/11, after `/speckit.analyze`: favourite, unfavourite, archive and unarchive update the screen at once and roll back if the server refuses. Delete stays confirmed, then waits for the server. Save character, Draw again submit and Delete show a spinner and stay disabled until the reply; optimistic actions don't.

## Why
Analyze finding C1 was fixed this way; the plan's Complexity Tracking exception for a non-optimistic star is removed, so no constitution change was needed.

## Alternatives considered
Keeping the star non-optimistic under a Complexity Tracking exception.

## Trade-offs accepted
Favourite and archive replies that omit picture fields keep the picture, drawing state and story count already on screen.

## Workflow detail
Applied in the 008 spec, plan and tasks (`4123f9f`) and implemented in `70282f4`.

## Related notes
[[2026-11-12-001]], [[use-one-character-detail-screen-for-both-profiles]]
