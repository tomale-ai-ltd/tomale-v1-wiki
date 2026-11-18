---
date: 2026-11-18
source: cursor
branch: 009-profiles-pin
feature: 009-profiles-pin
---

# Plan corrections for profiles and PIN

## What changed
- Kyle, 18/11: from a child profile, `PIN_NOT_SET` on a switch opens the locked screen as "Forgot your PIN?" with "Email me a link". Set PIN only from a parent session, because `POST /users/me/pin` is refused for a child.
- Help stays hidden until M7. Parent menu rows are Switch profile, Manage profiles, and Settings.
- Updated `specs/009-profiles-pin/plan.md`, `data-model.md`, and `copy.md`. No tasks. No commit.

## Decisions
- Kyle set both corrections. Cursor did not edit `spec.md` or `research.md`. Those still describe a Help row.

## Open questions / blockers
- `spec.md` FR-002 still requires the Help row. `research.md` still rejects hiding Help.

## Next
- Kyle runs `/speckit.tasks` after this.
