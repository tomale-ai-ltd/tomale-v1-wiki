---
date: 2026-11-26
source: cursor
branch: 011-story-creation
feature: 011-story-creation
---

# Constitution 1.6.4 PATCH — 011 live error codes

## What changed
- `.specify/memory/constitution.md` 1.6.3 → 1.6.4 (error-code list only).
- `.cursor/rules/tomale-api.mdc` live/planned lists matched.
- Live: `INVALID_CHARACTERS`, `INVALID_INPUT`, `STORY_NOT_EDITABLE`, `SAFEGUARDING_CONCERN`; `ENTITLEMENT_LIMIT_REACHED` moved from planned. Planned: none.
- Commit `2967595211c745a7d0fb99c88522bc00364e8051` (`docs: amend constitution to v1.6.4 (011 live error codes)`). Not pushed.

## Decisions
- Kyle requested the PATCH (011 story creation). Cursor chose PATCH (not MINOR): list-only, no principle change.

## Open questions / blockers
- None.

## Next
- `/speckit.specify` for 011.
