---
date: 2026-11-18
source: cursor
branch: 009-profiles-pin
feature: 009-profiles-pin
---

# Plan for profiles and PIN

## What changed
- Refreshed `.docs/prd/009-profiles-pin.md` from `Project/Plan/009-profiles-pin-micro-prd.md`. The two files match.
- Copied boards 901–908 and the avatar board from `Project/Design/009-profiles-pin/` into `specs/009-profiles-pin/design/`. The export has no PNGs.
- Wrote the plan, research, data model, copy, quickstart, and `contracts/profiles-pin.openapi.yaml`. Updated the Cursor speckit context. No commit.

## Decisions
- Kyle asked the plan to include the typed error overlay, kit ScreenHeader (RS-2026-11-17-03), and the 30 animal avatars (RS-2026-11-18-01). Those are implement steps. `overrides.yaml` and `ui.mdc` were not edited in this stop, and the client was not regenerated.
- Cursor chose the live Postman body `{ payload: { code, message, attempts_remaining? } }` for the overlay schema. HTTP 401 on a switch signs the person out with or without a code.
- Cursor chose mock-up words where the spec still had a placeholder: "Email me a link", "Those didn't match. Let's start again.", and the longer delete sheet. The tries-left sentences stay as the spec wrote them.
- The micro-PRD acceptance line that creates the child when the PIN is saved is not the rule. Kyle's 18/11 clarify answer stands: save stays off until a name and a picture are chosen.

## Open questions / blockers
- None for plan. The old-to-new avatar table is a fixed resolver constant; the note does not assign which old key maps to which animal.

## Next
- `/speckit.tasks` when Kyle asks. Implement then adds the overlay, runs `pnpm update:openapi`, adds `ScreenHeader`, and replaces `assets/avatars/`.
