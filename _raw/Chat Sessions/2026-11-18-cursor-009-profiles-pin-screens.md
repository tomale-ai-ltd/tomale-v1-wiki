---
date: 2026-11-18
source: cursor
branch: 009-profiles-pin
feature: 009-profiles-pin
---

# Compared the 009 screens with the boards and fixed two bugs

## What changed
- Captured the running development build with `pnpm shot` and compared it with `Project/Design/009-profiles-pin/`. Did not start, stop, or rebuild Metro or the simulator.
- `a423b4b` Keep the account email so Forgot PIN can send the unlock link. The signed-in user is not persisted, so Forgot PIN hid "Email me a link" and said the account had no email. Re-opened Forgot PIN after the fix: the button is there. No email was sent.
- `e3f62fe` Reset Set PIN when its mode changes. A second visit kept the previous step, so Change PIN showed "Choose a PIN" instead of "Enter your current PIN".
- Not pushed. The earlier avatar-key drop is still uncommitted and was not included in these commits.
- One wrong PIN was entered on the live account. The pad then said "That's not right. 4 tries left". The locked title was not opened. The simulator was left on the profile picker, signed in as Noah.

## Decisions
- Cursor treated spacing, size, and colour differences as snags and did not change them. The two commits are the behaviour bugs only.
- Cursor did not enter further wrong PINs, because that would lock the household PIN.

## Open questions / blockers
- Add profile with a name and picture chosen was not captured. The session was already the child, and a child is sent home from that form.
- Change PIN was not re-opened after the fix, for the same reason. Set PIN redirects a child session.

## Next
- Kyle can switch back to the parent with the PIN. Four tries were left after the one wrong entry.
- Snags are listed in the chat, not fixed.
