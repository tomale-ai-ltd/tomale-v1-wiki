---
type: decision
title: "track-cosmetic-snags-separately-from-bugs"
project: tomale-rn-v1
status: accepted
date: "2026-11-12"
related:
  - "[[2026-11-12-002]]"
  - "[[snags]]"
affects:
  - "[[operating-model]]"
features:
  - X-process
  - X-testing
---

# Decision: track-cosmetic-snags-separately-from-bugs

## What we decided

Kyle decided (12/11) that cosmetic snags found in device checks go to a snag list ([[snags]]) for a polish pass, while bugs are fixed before merge. The first entries are S-001 (page bands should run to the top of the screen) and S-002 (drawing line legibility over a picture); S-003 (sign-in and magic-link screens still use the platform button) followed.

## Why

Not discussed in session notes beyond the outcome: it let 008 Characters finish and merge the same evening while small visual defects were kept for a later pass.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Known cosmetic defects ship on `main` until the polish pass (planned before the M3 screens).

## Workflow detail

During a device check, each finding is classed as a bug (fixed before the PR merges) or a snag (logged in [[snags]] with area, severity and target, then fixed in a polish pass or with the next slice that touches the area).

## Related notes

[[2026-11-12-002]], [[snags]], [[roadmap]]
