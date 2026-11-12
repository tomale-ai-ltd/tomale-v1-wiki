---
date: 2026-11-12
source: cursor
branch: 008-characters
feature: 008-characters
---

# US7b complete; ready for the on-device check

## What changed
- `1143878` lets the empty-state button wrap. The label stays at the heading size, centres on a second line at 320px, and the button grows. At a simulated 1.5× text size the label stays inside the button and the page does not scroll sideways. Pushed.
- `4df1ab7` restyles the Create menu to the artboard. Pushed.
- `ff65753` stubs the confirmation toast in the auth-gate test so Jest can load the main layout. Pushed.
- `5831d0a` marks US6, US7a, and US7b done in `specs/008-characters/tasks.md`. T031 stays open. Pushed to `origin/008-characters`. No pull request.
- Lint, typecheck, and the test suite passed (13 suites, 69 tests).

## Decisions
- Kyle rejected the 320px font shrink. The label stays at the normal size and wraps, and the button grows in height.
- Kyle approved the Create menu. Make a story stays Coming soon.
- Web type is set in pixels, so Chrome's font-size setting does not change it. The large-text check multiplied computed font size and line height by 1.5, which matches Chrome's Very large setting.

## Open questions / blockers
- T031 is still open. Kyle runs the device checks in `specs/008-characters/quickstart.md` with `pnpm start`.

## Next
- Kyle's on-device check. Do not open a pull request until he asks.
