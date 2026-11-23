---
date: 2026-11-19
source: cursor
branch: 010-approvals
feature: 010-approvals
---

# Stack reset after sign-in, and Settings as a page

## What changed
- `9a36c1e` Leave Home under a route that opens after sign-in. `resumePendingRoute` clears the stack, replaces Home, then pushes the saved route. Used when the picker or the tabs layout resumes a pending route.
- `0cbab5f` Open Settings as its own page instead of a hidden tab. `app/(main)/settings.tsx` stays wrapped in `ParentOnly`. The avatar menu and `hrefForPending("settings")` point at it. Log out stays. The main stack shows the Settings header.
- `5db1238` Type that reset against the router’s route type so `pnpm check` accepts it.
- Not pushed. `pnpm check` passed. `pnpm test`: 18 suites, 118 tests passed.

## Decisions
- Cursor resets the stack on every pending-route resume, including a parent who is already signed in, so Home is what Back reaches.

## Open questions / blockers
- Kyle retests the signed-out link and the Settings page.

## Next
- Phone retest. Nothing is pushed.
