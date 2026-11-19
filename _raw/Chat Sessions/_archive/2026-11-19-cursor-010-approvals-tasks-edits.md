---
date: 2026-11-19
source: cursor
branch: 010-approvals
feature: 010-approvals
---

# Edits to the approvals task list

## What changed
- Edited `specs/010-approvals/tasks.md` only. Uncommitted. No speckit, Metro, simulator, or other files.

## Decisions
- Kyle: the parent-only check sits on the approvals layout and the Store and Settings tabs, not on the main layout. A child or signed-out `tomalerntest://approvals` must not render the inbox.
- Kyle: `pendingRoute` moves to `components/navigation/pendingRoute.ts` because files under `app/` are routes.
- Kyle: `approvalsStore.reset()` runs on profile switch and on sign-out. Cursor named the sign-out call as `store/AuthStore.ts` `signOut`, because that is the function the logout button and the session interceptor both use.
- Kyle: T014 and T023 skip the toast and Rejected inbox states and leave them for the phone pass.

## Open questions / blockers
- None.

## Next
- Kyle reviews the task list, then analyze when he wants it.
