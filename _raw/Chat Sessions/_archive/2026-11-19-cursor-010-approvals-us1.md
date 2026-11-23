---
date: 2026-11-19
source: cursor
branch: 010-approvals
feature: 010-approvals
---

# US1 approvals screens committed; shots not taken

## What changed
- `35a4109` Keep the approvals lists in memory and clear them on switch. T001–T006.
- `ff780e3` Let a parent open a held story and approve it. T007–T014. Not pushed.
- `pnpm check` passed (lint and typecheck). `pnpm test`: 18 suites, 110 tests passed.
- T014 named shots were not taken. The booted simulator opened onto the login screen (`userId` null). Naming a login screen as a board state would mislabel it.

## Decisions
- Cursor stopped after US1, as Kyle asked. Reject sends nothing. US2–US5 were not started.
- Cursor did not start, stop, or rebuild Metro or the simulator. Metro was already listening on 8081. The dev client was opened with the existing `tomalerntest` URL so the running bundle could load.
- Toast states `approved` and `approved-not-ready` were skipped for the phone pass.

## Open questions / blockers
- The simulator session is signed out, so Home, the avatar menu, the inbox, and review were not compared with the boards.
- Phone list (text size, under 30 seconds, parent-to-child, toasts, empty inbox, text-pending review) was not run.

## Next
- Sign in on the simulator Kyle already has running, then the remaining US1 shots can be taken once, without a re-shoot of a file that already exists. None exist yet.
- US2 is next when Kyle asks.
