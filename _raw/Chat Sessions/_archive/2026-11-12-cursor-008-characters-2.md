---
date: 2026-11-12
source: cursor
branch: 008-characters
feature: 008-characters
---

# Kit revised after review, still uncommitted

## What changed
- Rebuilt the dev kit at `app/dev/kit.tsx` from the Characters artboards. Tokens added in `global.css` for the sizes that were not on the scale (32px card radius, 22/26 tile type, 190 tile, 76 circle, 52 favourite, 56 row, 7px frame). No screen restyle. Not committed. Not pushed.

## Decisions
- Kyle rejected the first kit. Both create tiles use the dark text token (`on-accent`) in both themes. The story tile fill is the band token (`#ff6666`), so the dark label keeps contrast. The button spinner uses the label token (`on-primary` on the primary button).
- Cursor chose placeholder figures for the carousel card and story thumbs. The design `png/` folder is still empty.

## Open questions / blockers
- The description field has no error sentence in the copy. The kit shows "That description isn't allowed. Please try another." so the error line is visible. Kyle to confirm or replace that line.
- Kit is not approved. Do not start the Characters screens until Kyle says so.

## Next
- Kyle reviews the kit at localhost:8081/dev/kit in light and dark. Commit only after he approves. Do not push.
