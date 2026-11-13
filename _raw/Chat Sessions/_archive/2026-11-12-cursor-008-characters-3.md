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
- `63bd91a` makes the Create tab a page. The teal block, grey cards, scrim and sheet handle were the artboard's stand-in for the page behind the sheet. Heading, two larger tiles, and the note remain. Shots in `.screenshots/create-menu/`. S-001 and S-002 were left for a polish pass.
- `3ef2bc0` stops those tiles filling the screen. They size to the picture and the label, and the note sits under them.
- `854d2b7` marks T031 done for the parent device checks. Child checks are deferred to M3 because there is no profile switching yet. RS-2026-11-12-05 was already applied in `0608924`. Pull request: https://github.com/tomale-ai-ltd/tomale-rn-test/pull/27. Not merged.
- `41e20f4` renames `store/charactersStore.ts` back to `store/CharactersStore.ts` through a temporary name, and updates the imports. A case-only path does not check out on macOS.
- After 008 merged, local `008-characters` was deleted. `e336d49` on `008-characters-docs` commits the leftover speckit files: data model, client contract, requirements checklist, and the agent-context rule. Pull request: https://github.com/tomale-ai-ltd/tomale-rn-test/pull/28. Not merged.

## Decisions
- Kyle's device check: icons were blank because colour props received CSS variables. Cursor resolved the tokens in `constants/theme.ts` through `useThemeColor`.
- Filter chips: light active is ink `#2b1f1c` on page `#f8f8f8` (15.03:1); inactive is ink on card `#ffffff` (15.96:1). Dark active is page `#1d1715` on ink `#f6efeb` (15.57:1); inactive is ink on card `#2a2220` (13.70:1). Detail and panel text pairs that were checked also clear 4.5:1. The lowest was accent-text `#1b7b7a` on the page `#f8f8f8` at 4.75:1.
- RS-2026-11-12-05 was approved and applied on `008-characters`, the branch that already holds the UI guide (`RS-2026-11-12-03`). `git grep 'var(--' components app` finds two class-name uses of the 7px frame width, and no colour props.

## Open questions / blockers
- T031 is still open. Kyle re-checks on the phone with `pnpm start`.

## Next
- Pull request 28 is open and not merged. `test` passed on `e336d49`. Child device checks wait for M3. S-001 and S-002 wait for a polish pass.
