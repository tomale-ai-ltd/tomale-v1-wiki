---
date: 2026-11-17
source: cursor
branch: 009-profiles-pin
feature: 009-profiles-pin
---

# Specify 009 profiles and PIN

## What changed
- `main` was already up to date. PR #29 (`71b18ea`, regenerated client) and PR #30 (`c2ce720`, constitution 1.6.2) are ancestors of `HEAD`.
- Copied `Project/Plan/009-profiles-pin-micro-prd.md` to `.docs/prd/009-profiles-pin.md` unchanged, then `/speckit.specify` only. Branch `009-profiles-pin`. Commit `4fb8d97` holds the micro-PRD, `specs/009-profiles-pin/spec.md`, and the requirements checklist. No clarify, plan, or tasks.

## Decisions
- Cursor left layout, spacing, colour, and artwork to plan. There are no mock-ups yet.
- Cursor followed the live checks where they disagree with the micro-PRD's HTTP 400: unknown profile on switch is `PROFILE_NOT_FOUND` at HTTP 404 (Postman 6B-7); a second unlock email inside a minute is `RATE_LIMITED` at HTTP 429 (Postman 6C-9). The spec requires the code and the words, not those two 400s.
- Set PIN opens when adding a child with `pin_set` false, when a parent profile is chosen and no PIN is set, and after an unlock link leaves `pin_set` false on an account that has a child. A childless sign-in does not open it. After an unlock, the new PIN enters the parent profile and Home opens; the picker waits until the next cold start.
- No resend control: the client has `GET /auth/verify_email` with a token, and no resend request. `EMAIL_NOT_VERIFIED` is the sentence only.
- Help stays on the parent menu and does not open a screen. Settings opens the existing screen.

## Open questions / blockers
- No `[NEEDS CLARIFICATION]` markers. Claude reviews the spec against the micro-PRD and constitution 1.6.2 before clarify.
- The regenerated client types every refusal on these endpoints with an empty body. `payload.code`, `payload.message`, and `attempts_remaining` are not in `api/client.ts`. The micro-PRD's codes are unmapped until planning adds the overlay schema. `EMAIL_NOT_VERIFIED` is still a planned constitution code. Postman 6B-8 asserts HTTP 401 for a logged-out switch and does not assert `UNAUTHORIZED`.

## Next
- Claude checks the spec. Cursor stops here.
