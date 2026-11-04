---
date: 2026-11-04
source: cursor
branch: 007-foundations-session
feature: 007-foundations-session
---

# Specify 007 client session handling

## What changed
- Copied `Project/Plan/007-foundations-session-micro-prd.md` to `.docs/prd/007-foundations-session.md` in tomale-rn-test.
- Created branch `007-foundations-session` from `main` at `8339e23` (even with `origin/main`).
- Wrote `specs/007-foundations-session/spec.md` and `specs/007-foundations-session/checklists/requirements.md`. Quality checklist passed. Nothing committed.
- `/speckit.clarify` finished. Three answers are in `## Clarifications` / `### Session 2026-11-04`.
- `/speckit.plan` wrote `specs/007-foundations-session/plan.md`, `research.md`, `data-model.md`, `quickstart.md`, and `contracts/session.openapi.yaml`. Constitution check passed. Nothing committed. Tasks were not generated.

## Decisions
- Kyle: store the access credential's issue time on every successful refresh, replacing the previous time, so the 50-minute foreground check starts again from that refresh.
- Kyle: sign out on a 400 or 401 from refresh. Stay signed in only on a network error or a 5xx. Cursor applied the same sign-out to every other refresh failure, including a success that omits replacement credentials, so a broken refresh cannot leave later requests failing.
- Cursor assumed a missing issue time, including a session moved from ordinary storage, counts as due for refresh, and that refresh then stores the issue time.
- Kyle: the crash-report profile id comes from `GET /auth/me` `active_profile.id`. Profile switching stays out of scope. If that field is absent, the report includes the account id and omits the profile id.

## Open questions / blockers
- The checked-in `/auth/me` type has no `active_profile`. The plan reads `active_profile.id` with a type guard and does not hand-edit the generated contract.
- `@swc/helpers` 0.5.24 was published 2026-11-04, so RS-2026-11-04-01 waits until 2026-11-11.

## Next
- `/speckit.tasks` when Kyle asks.
