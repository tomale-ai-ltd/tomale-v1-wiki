---
date: 2026-11-12
source: cursor
branch: 008-characters
feature: 008-characters
---

# Specify and plan Characters

## What changed
- Copied `Project/Plan/008-characters-micro-prd.md` unchanged to `.docs/prd/008-characters.md` and committed it as `5515ed3` on `008-characters`. Not pushed.
- Wrote `specs/008-characters/spec.md` and the requirements checklist. Clarify finished 12/11.
- Plan artifacts: `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/characters.openapi.yaml`, and `tasks.md`. Cursor context updated. Not committed. Not pushed.

## Decisions
- Kyle asked the spec to follow the generated character types. Cursor treated `picture_status`, `stories_count`, and a nullable `cover_image` as the picture contract, including a redraw that still has the previous picture. Favourite and archive replies that omit those fields keep the picture, the drawing state, and the story count already on screen.
- Kyle, 12/11: one detail screen for both profiles. A grid tap or "See more" on the carousel panel opens it. The parent sees More (archive and delete). The child sees the same screen without More, and favourite and Draw again work there. The carousel panel stays short: actions plus up to 2 stories.
- Kyle, 12/11: tapping the card again or the panel's Close control closes the short panel. A swipe closes it and moves to the next character, whose panel stays closed.
- Kyle, 12/11: after archive or delete, the parent stays on the list they were using. The carousel centres the next character with its panel closed. The grid stays without that character. Detail returns to the list that opened it. A short confirmation says "[Name] archived" or "[Name] deleted", with no undo. Restore is Unarchive from the archived filter.
- Kyle, 12/11: grid search filters the characters already loaded, for the active or archived list on screen. A name matches when it contains the typed text, ignoring capitals. Typing does not request another list. No matches shows "No characters called '[text]'" with a control that clears the search.
- Planning kept story rows in the order they arrive, and it does not add a name or description length beyond non-empty. The server message still covers a refusal. The star waits for the server. No new native module.

## Open questions / blockers
- None.

## Next
- Implement when Kyle asks, starting at US1. Do not push until he asks.
