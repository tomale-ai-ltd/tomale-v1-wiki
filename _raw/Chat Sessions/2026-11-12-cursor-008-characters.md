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

## Decisions
- Kyle asked the spec to follow the generated character types. Cursor treated `picture_status`, `stories_count`, and a nullable `cover_image` as the picture contract, including a redraw that still has the previous picture. Favourite and archive replies that omit those fields keep the picture, the drawing state, and the story count already on screen.
- Kyle, 12/11: one detail screen for both profiles. A grid tap or "See more" on the carousel panel opens it. The parent sees More (archive and delete). The child sees the same screen without More, and favourite and Draw again work there. The carousel panel stays short: actions plus up to 2 stories.
- Kyle, 12/11: tapping the card again or the panel's Close control closes the short panel. A swipe closes it and moves to the next character, whose panel stays closed.
- Kyle, 12/11: after archive or delete, the parent stays on the list they were using. The carousel centres the next character with its panel closed. The grid stays without that character. Detail returns to the list that opened it. A short confirmation says "[Name] archived" or "[Name] deleted", with no undo. Restore is Unarchive from the archived filter.
- Kyle, 12/11: grid search filters the characters already loaded, for the active or archived list on screen. A name matches when it contains the typed text, ignoring capitals. Typing does not request another list. No matches shows "No characters called '[text]'" with a control that clears the search.
- Planning kept story rows in the order they arrive, and it does not add a name or description length beyond non-empty. No new native module.
- Kyle, 12/11, after analyze: favourite, unfavourite, archive, and unarchive are optimistic and roll back on refusal. Delete stays confirmed, then the server. The plan's Complexity Tracking exception for the non-optimistic star is removed. Detail polls with its own 10-minute window. The store keeps a selected id, set on create, and the carousel keeps it after refresh. Screen copy is `specs/008-characters/copy.md`. US3 checks layout and the missing More control. Favourite is checked at US4 and Draw again at US5. The empty-state button opening the form is checked at the US2 checkpoint. All characters screens use the theme text components, and tap targets stay 48 points.
- The copy file and the spec agree that "Make a story" and "Create a story with [Name]" stay on "Coming soon" until M4. Cursor did not treat that as a conflict.

## Open questions / blockers
- None. Device checks in `specs/008-characters/quickstart.md` are still to run on a phone.

## Next
- Kyle runs the device checks, then asks for a push. Do not push until he asks.
