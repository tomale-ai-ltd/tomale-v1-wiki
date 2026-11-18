---
date: 2026-11-18
source: cursor
branch: 009-profiles-pin
feature: 009-profiles-pin
---

# Old avatar key table dropped

## What changed
- `706cc72` Drop the old avatar key table. `resolveAvatarKey` keeps the 30 `preset:<animal>` keys, `character:<id>`, and `preset:bear` for anything else. Removed the old-key list from `data-model.md`, the old-key cases from T007, T008 and `.tests/avatar-key.test.ts`, and the old-key line from `quickstart.md`.
- Not pushed.

## Decisions
- Kyle asked for this as its own commit. Nothing else in the slice was changed.

## Open questions / blockers
- Same as the bug-fix note: handset check still open. Spec, plan and research still say Help is hidden until M7.

## Next
- Kyle's handset check on the development build.
