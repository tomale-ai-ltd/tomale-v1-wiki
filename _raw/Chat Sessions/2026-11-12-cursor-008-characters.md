---
date: 2026-11-12
source: cursor
branch: 008-characters
feature: 008-characters
---

# Carousel picture shift and the first carousel screen

## What changed
- The signed-in animation library was checked. Its parallax carousel needs Moti, a linear gradient, a demo font, and Faker. None of those were added.
- The carousel picture now slides across the extra width from `CarouselParallax.dc.html` (the art is 370 wide inside a 270 frame). Reduce Motion leaves that picture centred. Plain Reanimated only.
- The parent carousel and panel were restyled toward that artboard, and the child sizes toward `CharactersChild.dc.html`. The grid card was left as it is.
- Screenshots are in `.screenshots/carousel/` (git-ignored). The kit shots from the earlier review are still in `.screenshots/kit/`. Nothing was committed or pushed. T039 is still open.

## Decisions
- Kyle: no new packages. Take only the scroll-linked picture shift, then continue the carousel and panel, then stop for review.
- Cursor kept "See more about [Name]" on the panel because the spec still opens detail from there. The artboard has no such row.
- The parent favourite control is 48px rather than the artboard's 44, so the target stays at least 48. The child one stays 52.
- Search on the carousel heading opens the grid, which is where search already lives.

## Open questions / blockers
- Kyle's review of the carousel and panel screenshots. The dev preview is `/dev/carousel` because the Characters tab needs a sign-in.
- The page is the theme background, not the pink illustrated backdrop. Draw again uses the accent fill. There is no pale-mint token.
- "Coming soon" makes the story tile taller than the 72px artboard tile.

## Next
- Kyle reviews `.screenshots/carousel/`. Do not mark T039 done and do not push until he says so. The More sheet is the screen after that.
