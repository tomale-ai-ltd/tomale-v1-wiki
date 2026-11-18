---
type: decision
title: "wait-for-server-on-profile-changes"
project: tomale-rn-v1
status: accepted
date: "2026-11-18"
related:
  - "[[2026-11-18-001]]"
  - "[[make-character-favourite-and-archive-optimistic]]"
  - "[[009-profiles-pin-micro-prd]]"
affects:
  - "[[PRD-Profiles]]"
  - "specs/009-profiles-pin/plan.md"
  - "specs/009-profiles-pin/spec.md"
  - "constitution (Principle 4 optimistic UI, exception only)"
features:
  - F-profiles
---

# Decision: wait-for-server-on-profile-changes

## What we decided
Kyle, 18/11, during the 009 analyze fixes: profile create, rename, picture change and delete are not optimistic. Each waits for the server before the screen changes. Kyle widened the optimistic-UI exception from Cursor's proposal to every profile change.

## Why
Names are checked on the server, so an instant rename or create could briefly show a refused name. A child must not appear, and a profile must not disappear, before the server accepts.

## Alternatives considered
Optimistic create or rename, which would leave a refused name on screen, or a child when the save is refused or the form is left.

## Trade-offs accepted
A departure from constitution Principle 4 (optimistic UI on create, edit and read), recorded as the third Complexity Tracking row in `specs/009-profiles-pin/plan.md`. Sunset: this slice only; revisit if a later spec allows a pending profile row.

## Workflow detail
Applied in the 009 spec, plan, data model and tasks by Cursor (analyze fixes, 18/11). No constitution change.

## Related notes
[[2026-11-18-001]], [[make-character-favourite-and-archive-optimistic]], [[009-profiles-pin-micro-prd]]
