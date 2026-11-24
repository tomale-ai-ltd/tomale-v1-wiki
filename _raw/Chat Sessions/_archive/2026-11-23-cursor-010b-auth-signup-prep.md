---
date: 2026-11-23
source: cursor
branch: 010b-auth-signup
feature: 010b-auth-signup
---

# 010b prep and specify

## What changed
- Branch `010b-auth-signup` from `main` at `caee36f` (snag PR #33 already merged). Nothing committed.
- Copied `Project/Plan/010b-auth-signup-micro-prd.md` to `.docs/prd/010b-auth-signup.md` unchanged.
- Overlay: `POST /auth/signup` 400 codes `EMAIL_IN_USE` and `TERMS_REQUIRED`; `POST /auth/resend_verification` 200 `{sent: true}` and 400 codes `ALREADY_VERIFIED` and `TOO_SOON`; sign-up inputs `terms_accepted` and `terms_version`. Refusal fixtures in `.tests/fixtures/`. `pnpm update:openapi` and `.tests/openapi-overlay.test.ts` passed (18 tests).
- The live spec also makes the `GET /auth/verify_email` token required. That came through codegen with the rest of the export.
- `/speckit.specify` wrote `specs/010b-auth-signup/spec.md` and `specs/010b-auth-signup/checklists/requirements.md`. Checklist passed.
- `/speckit.clarify` recorded Kyle's six answers from 23/11, then his 24/11 answer: a child's locked create action opens a sheet saying "Ask a grown-up".
- `302627b` lets the OpenAPI overlay copy request-body properties, with `.tests/openapi-request-body.test.ts`. Overlay, fixtures, client, PRD, and the spec stay uncommitted for a second commit.

## Decisions
- Cursor: these refusals are `{ payload: { code, message } }` with the codes as enums. No `attempts_remaining`. Terms inputs stay optional and nullable, as published, so a missing tick can still return `TERMS_REQUIRED`.
- Cursor: the overlay merger now copies listed request-body properties onto the operation. Fixture messages are the ones in the published Xano stack.
- Kyle numbered this slice 010b. The feature script offered `011-auth-signup`. Cursor kept `010b-auth-signup` and removed the empty 011 branch, because 011 is story creation.
- Kyle, 23/11: `ALREADY_VERIFIED` confirms the email. Only `TOO_SOON` shows the wait sentence. "Send it again" starts off, counted from account creation. The creation lock covers every profile. A password refusal matches `payload.param` = "password". S-031's one back button is in this slice. "Sign in instead" fills the email.

## Open questions / blockers
- None.

## Next
- Second commit: overlay, fixtures, client, and PRD. Then `/speckit.plan`.
