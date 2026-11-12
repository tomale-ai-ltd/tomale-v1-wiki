---
date: 2026-11-12
source: cursor
branch: 008-characters
feature: 008-characters
---

# Carousel review fixes, then character detail

## What changed
- `dcf2e8b` fills the Make a character tile's art circle with white. Not pushed.
- `55c3c98` restyles the carousel and panel, including the review fixes. Not pushed.
- Detail is restyled to `CharacterDetail.dc.html` and is not committed. Shots are in `.screenshots/detail/`. Revised carousel shots are in `.screenshots/carousel/`.

## Decisions
- Kyle approved the kit, with the white art circle, and approved the carousel once the five review notes were fixed.
- Draw again's strong teal was not a contrast choice. It was a stand-in because the pale teal was not a token. It is now the artboard colour, `#d7f3f2`, in both themes, with the dark text token.
- The caret at the panel's top corner was a card corner showing past the rounded panel. The page colour covers that corner.
- Cursor kept "See more about [Name]" on the panel. Detail still opens from it, and from the grid.

## Open questions / blockers
- Kyle's review of detail. A child uses the same screen without More. Story rows have no "For Mia" line because the story list has no audience field.

## Next
- Kyle reviews `.screenshots/detail/`. Do not push. The next screen after detail is the grid.
