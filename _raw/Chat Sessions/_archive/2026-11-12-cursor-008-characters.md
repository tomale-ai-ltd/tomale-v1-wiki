---
date: 2026-11-12
source: cursor
branch: 008-characters
feature: 008-characters
---

# Specify and plan Characters

## What changed
- Copied `Project/Plan/008-characters-micro-prd.md` unchanged to `.docs/prd/008-characters.md` and committed it as `5515ed3` on `008-characters`. Not pushed.
- Wrote `specs/008-characters/spec.md` and the requirements checklist. Clarify finished 12/11. Plan artifacts: `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/characters.openapi.yaml`, and `tasks.md`.
- After analyze, Kyle asked for remediation. Cursor copied the vault copy file to `specs/008-characters/copy.md` and edited the spec, plan, and tasks. Commit `4123f9f` records the spec, plan, tasks, copy, research, and quickstart. Not pushed.
- Kyle then updated the vault copy (the three missing lines, and the child hint "Tap [Name] to see more."). Cursor refreshed `specs/008-characters/copy.md` and pointed FR-023 at those lines. Research and quickstart now describe the optimistic star and archive.
- Implemented Characters on `008-characters` through T030 and T032. T031 device checks are still for Kyle. The app code is commit `70282f4`. Not pushed. The stories share the list screen, the detail screen, and the store, so they are one commit.
- After device testing, Kyle asked for US6 (five bugs) and US7 (visual fidelity) as new tasks. US6 is commit `2f1e20f`: a confirmation toast above the tab bar, grid-only search and filters, pressed states, spinners on Save, Draw again, and Delete, safe-area insets on pushed screens, and picture crops that keep the head. US7 setup is commit `d922bf7`: the vault mock-up folder copied to `specs/008-characters/design/`, plus tasks T038–T047. `png/` was empty, so the commit keeps the folder with `.gitkeep`. Not pushed. Screen restyling has not started.
- Kyle asked to apply approved repo-sync items RS-2026-11-12-02 and RS-2026-11-12-03 on `008-characters` before the component kit. Both notes have `status: approved`. Commit `493aef0` adds `scripts/sim-shot.sh`, `pnpm shot`, and ignores `.screenshots/`. Commit `1b23bfe` replaces the screenshot note with `.cursor/rules/ui.mdc`, a working guide for Principles 2 and 4. It adds no new principles or quality gates. Not pushed. No simulator had `com.tomaleai.tomalerntest` installed, and none was booted, so `pnpm shot test characters` exited before writing a PNG.

## Decisions
- Kyle asked the spec to follow the generated character types. Cursor treated `picture_status`, `stories_count`, and a nullable `cover_image` as the picture contract, including a redraw that still has the previous picture. Favourite and archive replies that omit those fields keep the picture, the drawing state, and the story count already on screen.
- Kyle, 12/11: one detail screen for both profiles. A grid tap or "See more" on the carousel panel opens it. The parent sees More (archive and delete). The child sees the same screen without More, and favourite and Draw again work there. The carousel panel stays short: actions plus up to 2 stories.
- Kyle, 12/11: tapping the card again or the panel's Close control closes the short panel. A swipe closes it and moves to the next character, whose panel stays closed.
- Kyle, 12/11: after archive or delete, the parent stays on the list they were using. The carousel centres the next character with its panel closed. The grid stays without that character. Detail returns to the list that opened it. A short confirmation says "[Name] archived" or "[Name] deleted", with no undo. Restore is Unarchive from the archived filter.
- Kyle, 12/11: grid search filters the characters already loaded, for the active or archived list on screen. A name matches when it contains the typed text, ignoring capitals. Typing does not request another list. No matches shows "No characters called '[text]'" with a control that clears the search.
- Planning kept story rows in the order they arrive, and it does not add a name or description length beyond non-empty. No new native module.
- Kyle, 12/11, after analyze: favourite, unfavourite, archive, and unarchive are optimistic and roll back on refusal. Delete stays confirmed, then the server. The plan's Complexity Tracking exception for the non-optimistic star is removed. Detail polls with its own 10-minute window. The store keeps a selected id, set on create, and the carousel keeps it after refresh. Screen copy is `specs/008-characters/copy.md`. US3 checks layout and the missing More control. Favourite is checked at US4 and Draw again at US5. The empty-state button opening the form is checked at the US2 checkpoint. All characters screens use the theme text components, and tap targets stay 48 points.
- The copy file and the spec agree that "Make a story" and "Create a story with [Name]" stay on "Coming soon" until M4. Cursor did not treat that as a conflict.
- Kyle, 12/11, after device testing: confirmations are a toast over the tab bar for about 3 seconds, announced to a screen reader, and never inline. Search and filters apply only to the grid. The carousel always shows active characters, favourites first. Grid All is active only. Archived appears only under Archived. Every tappable control shows a pressed state. Save character, Draw again submit, and Delete show a spinner and stay disabled until the reply. Optimistic actions do not. Pushed screens respect the safe area. Pictures are not cropped through the head.
- Kyle, 12/11: visual fidelity copies the mock-up folder into the spec and then matches one screen at a time, in this order: carousel and panel, More sheet, detail, grid, create form, Draw again sheet, delete confirmation, empty state, Create menu. After each screen, stop for a screenshot comparison. Colours come from theme tokens, not hard-coded hex. The PNGs are the visual target and the `.dc.html` files are the exact values. Cursor copied the folder and wrote the tasks, and did not restyle a screen in this session.
- Kyle, 12/11: US7 starts with a component kit in `components/ui/` (Card, ActionTile, BottomSheet, Toast, PressableScale, Button with a loading state), a dev-only route, and `pnpm shot` in light and dark, then stops for review. Screens are rebuilt from the kit only after he approves it. Cursor has not started the kit. The PNG re-copy is also waiting, because no simulator development build is installed.

## Open questions / blockers
- `specs/008-characters/design/png/` has no renders yet. Kyle exports them when the visual comparison needs them.
- T031, the original quickstart device checks, is still open.

## Next
- Kyle reviews the US7a kit at `http://localhost:8081/dev/kit` (web, 390×844, light and dark). It is not committed. Do not rebuild Characters screens until he approves the kit. Do not push. Do not change `eas.json`. The local `EX_DEV_CLIENT_NETWORK_INSPECTOR=false` stays. Simulator work is stopped. The vault `png/` folder was still empty.
