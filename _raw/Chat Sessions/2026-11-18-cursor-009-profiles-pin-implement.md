---
date: 2026-11-18
source: cursor
branch: 009-profiles-pin
feature: 009-profiles-pin
---

# Implemented profiles and PIN through editing

## What changed
- User Story 1 was already in the working tree: header band, animal avatars, profile list, switch, PIN pad, and the manage stub.
- Added the cold-start and 15-minute picker gate, the locked and forgot screen, Set PIN and Change PIN, manage, add, edit, and delete. Unlock email uses `purpose: reset_pin`. A magic link with `pin_set` false and a child opens Set PIN.
- `pnpm check` passed. The profile, avatar, overlay, and magic-link tests passed (31). The phone pass and screenshots are still open.

## Decisions
- Cursor kept the picker over the tabs until a switch succeeds, and hid it while Set PIN is open, so a forced picker can still reach Set PIN.
- Cursor did not start Metro or the simulator. Kyle is building the development client.

## Open questions / blockers
- Screenshots against the boards, and the phone pass, wait until the development build is ready.

## Next
- Walk the quickstart on the simulator and on Kyle's phone. Do not commit `.screenshots/`.
