---
date: 2026-11-24
source: cursor
branch: 010b-auth-signup
feature: 010b-auth-signup
---

# 010b phone-pass bugs

## What changed
- `ca572a0` clear household caches across accounts; Name step waits for this session's profiles.
- `b524b0e` Set PIN not from a cold-start tap of the active parent.
- `05cb7eb` wrong password → Invalid credentials (400 and 401).
- `9da97a6` Sign in autofill survives Face ID; no signed-out refresh/recheck.
- `4e94316` Sign in reads /auth/me before the token flips the guards (no blank frame).
- `c20ec4f` unconfirmed hold keeps Check your email during a foreground refetch.
- Not pushed. Typecheck and the related Jest suites green.

## Decisions
- Cursor: profiles are no longer restored from AsyncStorage across launches; `loadProfiles` fills them after the signed-in account is known.
- Cursor: tapping the already-active parent on the picker with `pin_set` false enters Home; Set PIN stays for switch / add child / unlock.

## Open questions / blockers
- The me output list still needs `email_ver_expires_at` on the Xano side.

## Next
- PR when Kyle asks.
