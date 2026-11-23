---
date: 2026-11-20
source: cursor
branch: 010-approvals
feature: 010-approvals
---

# Sign-in handover no longer leaves the picker to run twice

## What changed
- `89ddcec` Replace sign-in with the app, and resume a saved route inside it. Password login (`useAuth.login` and bootstrap) and the magic-link `auth/complete` path use `replaceSignedIn`: if auth screens can be dismissed they are dropped, then the app replaces the focused screen. `resumePendingRoute` no longer calls `dismissAll`. It replaces Home and pushes the saved route.
- The “picker already passed” memory was not added. Resume no longer leaves the main layout.
- Not pushed. `pnpm check` passed. `pnpm test`: 18 suites, 121 tests passed.

## Decisions
- Kyle agreed the second picker came from `dismissAll` unmounting the main app, and asked to fix the handover first rather than remember that the PIN had been entered.

## Open questions / blockers
- Kyle retests the signed-out approvals link.

## Next
- Phone retest. Nothing is pushed.
