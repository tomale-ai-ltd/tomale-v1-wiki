---
date: 2026-11-12
source: cursor
branch: 008-characters
feature: 008-characters
---

# Carousel gap, detail Favourite, then the grid

## What changed
- `f732a57` lets the page colour show between the carousel cards. The darker strip was the card shadow filling the gaps.
- `815e457` restyles character detail. Favourite is yellow with a filled star, or a white pill with the border token and an outline star.
- Both commits are on `origin/008-characters`. No pull request.
- The grid is restyled to `Characters.dc.html` and is not committed. Shots are in `.screenshots/grid/`. Revised carousel and detail shots are in `.screenshots/carousel/` and `.screenshots/detail/`.

## Decisions
- Kyle asked for the page colour to run through the card row, so the carousel cards no longer carry the large drop shadow.
- The unfavourited pill uses the border token and stays white in both themes. The label stays "Favourite".
- The detail header buttons keep their top inset.
- The grid search placeholder stays "Search characters", from the copy sheet.

## Open questions / blockers
- Kyle's review of the grid. A child still never sees it.

## Next
- Kyle reviews `.screenshots/grid/`. Do not push again until he asks. The next screen after the grid is the create form.
