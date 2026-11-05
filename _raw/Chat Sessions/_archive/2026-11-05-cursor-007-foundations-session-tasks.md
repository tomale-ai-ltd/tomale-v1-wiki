---
date: 2026-11-05
source: cursor
branch: 007-foundations-session
feature: 007-foundations-session
---

# Tasks for 007 client session handling

## What changed
- Wrote `specs/007-foundations-session/tasks.md` from the plan, spec, research, data model, session contract, and quickstart. 25 tasks, T001–T025. Nothing committed. Implementation has not started.

## Decisions
- Jest tasks are included because the plan, quickstart, and constitution require automated auth checks. US3 persistence stays a device check.
- The `@swc/helpers` override is an explicit non-change until 2026-11-11.

## Open questions / blockers
- None for the task list. `active_profile.id` is still read with a type guard.

## Next
- Implement when Kyle asks, starting at T001. MVP stops after User Story 1 if he wants that checkpoint.

## Amendment 2026-11-05
- Kyle: a refresh timeout or HTTP 429 must not sign the parent out. Same as a network error or a 5xx: stay signed in, keep issuedAt, show the action's error.
- Updated FR-012 and the matching spec sentences, plan.md, T012 (429 moved out of the sign-out cases; Jest cases added for timeout and 429), plus research, data model, session contract, and quickstart so they do not still say 429 signs the parent out. No code implemented.
- Applied analyze remediations in spec.md, plan.md, and tasks.md only. Foreground refresh stays the 50-minute rule; plan records RS-2026-11-05-02 for a constitution clarification after merge. Stay-signed-in set is network error, timeout, 429, and 5xx. FR-001 stores session id only when the body includes it. Account creation is out of this slice. Added T014 for secure-session storage tests and renumbered through T026. T013 signOut clears Sentry identity. Removed the incorrect parallel markers. No app code.
- Follow-up on the second analysis: plan summary stores session id only when the success body includes it. T021 depends on T016 and T019. The User Story 1 checkpoint is a test stop and must not be shipped, because the session stays in AsyncStorage until T016.

## Implementation 2026-11-05
- Kyle: MVP only, T002–T011. Do not install expo-secure-store by bypassing the release-age gate. T001 moves to just before T014, after 2026-11-06. No PR.
- package.json and the lockfile were left unchanged. The earlier secure-store line was reverted.
- Session store now has refreshToken, sessionId, issuedAt, profileId, applySession, and signOut. The HTTP client is Axios, attaches the bearer, and shares one refresh. Login, magic-link completion, the home screen, and foreground resume use that path. Bookshelf was already correct.
- `.tests/session-refresh.test.ts` and `.tests/smoke.test.ts`: 7 passed. Sign-out on a bad refresh is still T012–T013. SecureStore is still T001 then T014.
- Commits on 007-foundations-session, not pushed: `76dadd1` docs, `d637138` User Story 1 code and tests.
- User Story 2: refresh 400/401/403/404, a 200 missing credentials, and a protected 401 with no refresh credentials sign out once and clear Sentry. Network, timeout, 429, and 5xx stay signed in. Requests time out at 20s, refresh at 10s, and refresh sends no bearer. A stale 401 retries the current token without refreshing. Foreground refresh applies those rules and does not reject unhandled. Session tests plus smoke: 19 passed.
- Committed User Story 2 locally as `b340b27`. Not pushed.
- User Story 4 without secure storage: Sentry beforeSend keeps `user.id` and drops email, username, IP, and an Authorization header. `readActiveProfileId` reads `active_profile.id`. Sign-in and bootstrap store that id, or clear it when the response has none. T021 still waits on T016.
- Magic link: the address `authToken` is ignored. Sign-in completes only from `POST /auth/complete_magic_link` with the link token, then stores `active_profile.id` from `GET /auth/me`. A missing id clears the profile id and leaves the account id. Jest could not render the screen (React Native mapper), so the checks call `completeMagicLink` directly. Magic-link, Sentry, session, and smoke: 25 passed.
- Committed that User Story 4 work, including T017 and T023, locally as `489b0b2`. Not pushed. Left for 2026-11-06: T001, T014–T016, T021, T024–T026.
- Kyle asked for a backup push and no PR. Working tree was already clean, so no new commit. Lint, typecheck, and 25 tests passed. Pushed `007-foundations-session` to origin and set the upstream. Tip remains `489b0b2`. No pull request.
