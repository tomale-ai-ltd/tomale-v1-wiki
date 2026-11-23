---
date: 2026-11-23
source: cursor
branch: polish-snags
feature: polish-snags, RS-2026-11-18-02
---

# Polish snags on headers, picker, PIN, and controls

## What changed
- Branch `polish-snags` from `main`. Not pushed. One commit per snag, plus `2086ea3` so the picker lock badge uses the `warning-surface` class (typecheck).
- Group 1: `6d471a6` S-001, `3041b9e` S-017, `b297a5c` S-018, `41edb92` S-022.
- Group 2: `bf0d804` S-005, `824f825` S-006, `564ca17` S-007, `1308eed` S-008, `23582e3` S-009, `5962b56` S-010, `f4d7036` S-011, `a3be877` S-012, `94f3785` S-013, `115a481` S-015, `b00174a` S-016.
- Group 3: `aa262d2` S-002, `3da0597` S-019, `de56f08` S-020, `af3e34a` S-021.
- `b6ab242` RS-2026-11-18-02: 009 spec, plan, research, and tasks list Help on the parent menu. Help closes the sheet and opens no screen. `data-model.md` had no Help lines. No app change.
- Left alone: S-003, S-004, S-014.
- `pnpm check` and `pnpm test` passed (18 suites, 121 tests). No simulator was booted, so shots were skipped.

## Decisions
- Kyle: greeting is Home only. Recorded in `.cursor/rules/ui.mdc`.
- Cursor: cream page and lock-badge border use `warning-surface`. Waiting OK and the picker highlight use `band` (coral). Reject story and Delete stay danger.
- Cursor: Characters grid and empty put the profile row inside a page `ScreenHeader`. Carousel keeps the framed header.

## Open questions / blockers
- Phone check still needed. Snag status in the vault was not updated.

## Next
- Kyle checks the screens on a phone, light and dark. No PR until he asks.
