---
type: decision
title: "run-one-phone-pass-at-the-end-of-each-slice"
project: tomale-rn-v1
status: accepted
date: "2026-11-24"
related:
  - "[[2026-11-24-003]]"
  - "[[check-every-screen-on-the-phone-before-done]]"
  - "[[track-cosmetic-snags-separately-from-bugs]]"
affects:
  - "[[operating-model]]"
features:
  - X-testing
  - X-process
---

# Decision: run-one-phone-pass-at-the-end-of-each-slice

## What we decided

Kyle, 24/11: drop routine mid-slice phone pauses. Each slice gets one full phone pass at the end, with a mid-slice smoke test on the phone only for risky foundational changes (navigation guards, auth/session, data shape). A screen still isn't done until Kyle has seen it on the phone ([[check-every-screen-on-the-phone-before-done]]); this sets when that check happens.

## Why

Not discussed in session notes. The 010b slice ran this way on 24/11: one full phone pass at the end found six bugs (stale household data across accounts, Set PIN on cold start, wrong-password copy, Face ID wiping autofill, a blank frame from Sign in to Name, Check your email leaving on a screenshot), fixed in one bug round before the merge.

## Alternatives considered

Routine phone pauses during a slice (the earlier practice).

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

In a speckit slice, Cursor implements through to the end and Kyle runs one full phone pass before the PR is merged; bugs it finds are fixed before merge and cosmetic findings go to [[snags]]. Cursor or Claude asks for a mid-slice smoke test only when a change touches navigation guards, auth or session handling, or the shape of data. CURRENT's 011 plan already says "one phone pass at the end".

## Related notes

[[2026-11-24-003]], [[check-every-screen-on-the-phone-before-done]], [[track-cosmetic-snags-separately-from-bugs]], [[operating-model]], [[snags]]
