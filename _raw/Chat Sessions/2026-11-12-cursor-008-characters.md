---
date: 2026-11-12
source: cursor
branch: 008-characters
feature: 008-characters
---

# Specify Characters

## What changed
- Copied `Project/Plan/008-characters-micro-prd.md` unchanged to `.docs/prd/008-characters.md` and committed it as `5515ed3` on `008-characters`. Not pushed.
- Wrote `specs/008-characters/spec.md` and `specs/008-characters/checklists/requirements.md`. Those two files are not committed. Clarify and plan were not run.

## Decisions
- Kyle asked the spec to follow the generated character types. Cursor treated `picture_status`, `stories_count`, and a nullable `cover_image` as the picture contract, including a redraw that still has the previous picture. Favourite and archive replies that omit those fields keep the picture, the drawing state, and the story count already on screen.

## Open questions / blockers
- One `[NEEDS CLARIFICATION]` remains: how someone opens the character detail screen (grid only, grid and carousel, or the carousel panel is the detail screen).

## Next
- Kyle answers that question. Then `/speckit.clarify` or `/speckit.plan`. Do not push until he asks.
