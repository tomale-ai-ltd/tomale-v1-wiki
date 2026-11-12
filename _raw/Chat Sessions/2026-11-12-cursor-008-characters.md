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
- Kyle, 12/11: one detail screen for both profiles. A grid tap or "See more" on the carousel panel opens it. The parent sees More (archive and delete). The child sees the same screen without More, and favourite and Draw again work there. The carousel panel stays short: actions plus up to 2 stories.

## Open questions / blockers
- None left in the spec.

## Next
- `/speckit.clarify` or `/speckit.plan` when Kyle asks. Do not push until he asks.
