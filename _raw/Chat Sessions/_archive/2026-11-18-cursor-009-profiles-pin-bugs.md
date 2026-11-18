---
date: 2026-11-18
source: cursor
branch: 009-profiles-pin
feature: 009-profiles-pin
---

# Three picker and menu bugs committed, not pushed

## What changed
- `940818c` Show Help on the parent avatar menu. Help closes the sheet and does not open a screen. Approvals stays out. Child menu is still Switch profile only. `specs/009-profiles-pin/copy.md` parent rows now include Help.
- `965cc14` Keep a freshly loaded profile list ahead of the saved copy. `noteProfilesLoaded` plus persist `merge` so a late rehydrate cannot put the saved list back over a list loaded this session.
- `84ee763` Mark grown-up profiles with the lock badge on the picker. Theme tokens, grown-ups only.
- Not pushed. No PR. T034 still open.
- Left uncommitted (Kyle has not asked to commit it): the old-key drop in `avatarKey.ts`, `.tests/avatar-key.test.ts`, `data-model.md`, `quickstart.md`, `tasks.md`.

## Decisions
- Kyle updated user 66's `user_profile.avatar_key` himself (Kyle bear, Noah turtle, Reuben fox, Freya Bean cat). Cursor did not write to Xano. An earlier metadata write was aborted and was not retried.
- The bears were empty `avatar_key` values on those user 66 rows. The saved store matched the table. User 135's animals are a different account. After Kyle's update, a picker refetch showed the four animals and the store kept those four strings. The persist guard is so a saved empty list cannot overwrite that response later in the same session.
- Help follows the micro-PRD (Switch profile, Manage profiles, Settings, Help). Spec, plan, research and tasks still say Help is hidden until M7. copy.md was updated with the menu commit. Spec was not rewritten.

## Open questions / blockers
- Kyle will confirm Help, the four pictures (picker, Manage, header) and the lock on the handset. Header and Manage were not re-shot after the refetch. Simulator was left on the picker. Session may still be Noah. One wrong PIN was entered earlier; 4 tries were left. Do not guess the PIN or send an unlock email.
- Screenshot snags from the earlier pass stay unfixed: picker one column, missing corner shapes, cream vs theme surface; add form missing the hero preview and pill tabs; Set PIN eyebrow and gold band; locked and forgot screens missing the large illustration; child Switch profile is a list row, not a red pill; parent menu rows lack the board's icon circles and chevrons.

## Next
- Kyle's handset check on the development build. Then decide whether to commit the old-key drop and whether to update spec.md so Help matches the menu.
