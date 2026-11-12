---
date: 2026-11-12
source: cursor
branch: 008-characters
feature: 008-characters
---

# Device-check fixes pushed for a phone re-check

## What changed
- `972e0e1` resolves theme colours for SVG and Lucide props. `var(--token)` is blank on iOS.
- `5e4d069` opens More, Draw again, and delete on the kit sheet. The old More menu is deleted. Draw again and delete keep their approved panels inside that sheet.
- `18426ca` sets filter-chip colours per theme.
- `52cbccd` drives the pagination dots from the scroll position on the UI thread, and caches card pictures with expo-image.
- `a0d337f` lifts Draw again, delete, and the create form above the keyboard. Pushed to `origin/008-characters`. No pull request. T031 stays open.
- Lint, typecheck, and tests passed (13 suites, 69 tests).
- `0608924` applies RS-2026-11-12-05 to `.cursor/rules/ui.mdc`: no CSS variables in native colour props, keyboard avoidance, and a phone check before a screen is done. Pushed on `008-characters`, with the device-check fixes. No pull request. The item status in the vault was left for Kyle or Claude.

## Decisions
- Kyle's device check: icons were blank because colour props received CSS variables. Cursor resolved the tokens in `constants/theme.ts` through `useThemeColor`.
- Filter chips: light active is ink `#2b1f1c` on page `#f8f8f8` (15.03:1); inactive is ink on card `#ffffff` (15.96:1). Dark active is page `#1d1715` on ink `#f6efeb` (15.57:1); inactive is ink on card `#2a2220` (13.70:1). Detail and panel text pairs that were checked also clear 4.5:1. The lowest was accent-text `#1b7b7a` on the page `#f8f8f8` at 4.75:1.
- RS-2026-11-12-05 was approved and applied on `008-characters`, the branch that already holds the UI guide (`RS-2026-11-12-03`). `git grep 'var(--' components app` finds two class-name uses of the 7px frame width, and no colour props.

## Open questions / blockers
- T031 is still open. Kyle re-checks on the phone with `pnpm start`.

## Next
- Kyle's on-device re-check. Do not open a pull request until he asks.
