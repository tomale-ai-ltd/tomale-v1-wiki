---
date: 2026-11-19
source: cursor
branch: 010-approvals
feature: 010-approvals
---

# Phone-pass fixes for the approvals slice

## What changed
- Eleven commits on `010-approvals`, not pushed. Snags S-019 and S-020 left alone. No speckit commands, no Metro or simulator changes, no screenshots.
- `8db3f41` Keep the PIN picker up when the app is only briefly inactive. Foreground can raise the picker and cannot lower it. Only entering through the PIN sets the gate to the app.
- `0254d21` Decide the profile picker once per sign-in, not on every new token. A second tap on a child while a switch is running does nothing.
- `31a5bba` Open a signed-in session even before a user id is stored. The first version of the sign-in key waited for a user id, so the existing gate test never showed the app. A later token still does not raise the picker.
- `f59d7d3` Open Settings from the avatar menu. `href: null` marked the tab hidden, and the navigator sent the parent back to Home. The tab button is hidden without unregistering the route. `ParentOnly` was not the block.
- `68c0a64` Dismiss Coming soon on the same three-second timer as the approve toasts. Toast text uses the theme ink on the theme card, so dark mode is light ink on the dark card.
- `c1ad261` Show which approvals segment is selected, with `accessibilityState.selected`.
- `6bbd97b` Return to the approvals inbox already on the stack, via `dismissTo` instead of `replace`.
- `4c111d9` Clear the approve error when a retry starts and when it succeeds.
- `d12ffee` Show a friendly retry when a story fails to load. No sections, name, or approve buttons, and no raw error.
- `811f2b7` Say your child when a sentence has no profile name. Row labels stay "A story".
- `3dac4eb` Show the year on dates outside this year.
- `pnpm check` passed. `pnpm test`: 18 suites, 117 tests passed.

## Decisions
- Cursor keyed the cold-start picker on the sign-in, not the user id, because a token can exist before the user id is stored and a replacement token must not raise the picker.
- Cursor hid Settings with `tabBarButton: () => null` rather than moving the screen, because the existing Settings screen and Log out stay, and the tab stays off the bar.

## Open questions / blockers
- Kyle retests on the phone. T029 is still his.

## Next
- Kyle walks the phone list, including the ten fixes and steps 5 and 6. Nothing is pushed.
