---
date: 2026-11-24
source: cursor
branch: 010b-auth-signup
feature: 010b-auth-signup
---

# 010b prep commit

## What changed
- `358f454` on `010b-auth-signup`: sign-up and resend-verification refusals, fixtures, generated client, PRD, and spec. Not pushed.
- Added `.tests/fixtures/post-auth-signup-weak-password.json` from Postman 8A-5: `ERROR_CODE_INPUT_ERROR` with `payload.param` = "password". The overlay test lists it with the other four refusal fixtures.
- Sign-up 400 in the overlay is now the coded refusal (`EMAIL_IN_USE`, `TERMS_REQUIRED`) or that password input error. `pnpm update:openapi` wrote `api/openapi/xano.yaml` and `api/client.ts`.
- Overlay and request-body tests: 2 suites, 20 tests passed. `pnpm typecheck` passed.

## Decisions
- Cursor: the weak-password body stays out of the domain-code enum. The app matches `payload.param` only, never the message. The overlay records both 400 shapes so the fixture matches the generated spec.

## Open questions / blockers
- None.

## What changed (later the same day)
- `6c68343` on `010b-auth-signup`: constitution 1.6.2 → 1.6.3 and `.cursor/rules/tomale-api.mdc`. Error-code lists only. Not pushed.
- Live and planned lists are identical in both files (29 live, planned `ENTITLEMENT_LIMIT_REACHED`). Fixture domain codes are on the live list. `ERROR_CODE_INPUT_ERROR` in the weak-password fixture is the input-error envelope, not a listed code.
- Live additions: `CANNOT_DELETE_PRIMARY`, `CONTENT_REJECTED`, `NOTHING_TO_UPDATE`, `IMAGE_JOB_IN_PROGRESS`, `EMAIL_IN_USE`, `TERMS_REQUIRED`, `ALREADY_VERIFIED`, `TOO_SOON`, plus `EMAIL_NOT_VERIFIED` moved from planned. Also from merged spec 009: `CANNOT_DELETE_ACTIVE`, `INVALID_NAME`, `INVALID_AVATAR_KEY`, `ACCOUNT_LIMIT_REACHED`, `PROFILE_NOT_FOUND` (HTTP 404), `RATE_LIMITED` (HTTP 429).
- Not added: `STORY_NOT_EDITABLE` (not asserted), `UNAUTHORIZED` (009 says the 401 check does not send it). A weak password stays an input error (`payload.param` = "password"), not a code.
- Before the commit: `pnpm lint` passed and `pnpm test` passed (19 suites, 126 tests).

## What changed (plan)
- `/speckit.plan` for 010b. `setup-plan.sh` rejected branch `010b-auth-signup` (it wants `001-feature-name`). The plan was written at `specs/010b-auth-signup/` anyway. Artifacts: `plan.md`, `research.md`, `data-model.md`, `copy.md`, `quickstart.md`, `contracts/auth-signup.openapi.yaml`. Agent context updated.
- `b1f1adf` commits those plan artifacts and `.cursor/rules/specify-rules.mdc`. Not pushed.
- `GET /auth/me` does not return `email_ver_expires_at` today. The wait formula is in the plan. Kyle adds the column to the Xano me output. Cursor does not edit Xano.

## What changed (speckit prefix)
- `b89c800` on `010b-auth-signup`: `.specify/scripts/bash/common.sh` accepts `^[0-9]{3}[a-z]?-`. Directory lookup uses the full prefix, so `010b` resolves to `specs/010b-auth-signup` and `010` still resolves to `specs/010-approvals`. Not pushed. Re-apply this after a speckit upgrade.

## What changed (tasks)
- `2488275` on `010b-auth-signup`: `specs/010b-auth-signup/tasks.md` (38 tasks) and the cold-start failure sentence in `plan.md`. Not pushed.
- `RESEND_THRESHOLD_SECONDS` is 86340 and comments `auth_send_verification_email` and `auth_resend_verification_POST`. Cold start waits for `/auth/me` and, on failure, stays signed in with creating locked. One task per S-031 back control (T028–T037). Tests cover each of the five refusal fixtures and the wait at 0, 59, and 61 seconds since send.
- Analyze fixes in that commit: T036 follows T021 on `CharacterDetailBody.tsx`. T026 keeps a route email so "Sign in instead" stays filled in. T012 covers the keyboard, Return, and offering the new password. The leave-alone list names the unavailable character's "Back to characters" text and the profile picker's "Close" X.

## What changed (implement, MVP)
- T001–T014 on `010b-auth-signup`, not pushed. `32af4ce` legal URLs. `2a2d1ba` `email_ver_expires_at` on the overlay and generated client. `1d708e9` `payload.param`. `a1e3f37` refusal mapping and the 86340-second wait. `8698953` one shared account refetch. `3dd9f6e` kit back button. `306ff5b` route guards, cold-start failure stays signed in with creating locked, Create account, Check your email.
- Overlay and signup-rules tests passed (2 suites, 29 tests). `pnpm typecheck` passed. Metro was not started.
- "Send it again" posts nothing yet (T015). If `/auth/me` still omits `email_ver_expires_at`, the control is available because a null expiry does not invent a wait.

## What changed (sign-up handover)
- `d56c8a4` on `010b-auth-signup`: Check your email opens from `signUp` after `/auth/me`, before the token is stored. Create account no longer navigates from an effect that unmounts with the signed-out guard. Cold start still opens the Name step when `onboarding_complete` is false. Not pushed. Typecheck and the overlay and signup-rules tests passed.

## What changed (US2)
- `a5cb0d7` skips `dismissAll` on the sign-up handover so `POP_TO_TOP` is not dispatched after the signed-out guard has removed `(auth)`. Sign-in still drops a stack that is mounted.
- `66019e6` T015: Send it again posts `/auth/resend_verification`. `0916bf1` T016 T017: `app/auth/verified.tsx`, the foreground recheck, the one "Email confirmed" toast, and the parent and child confirm sheets. `2249af1` T018–T022: Create, Home, and Characters stay locked until the email is confirmed. Not pushed.
- `pnpm typecheck` passed. Signup-rules, overlay, and approvals-rules tests passed (3 suites, 52 tests). Metro was not started.

## Next
- Phone check for US2, then stop. T023 is next when Kyle asks. The me output list still needs `email_ver_expires_at` on the Xano side.
