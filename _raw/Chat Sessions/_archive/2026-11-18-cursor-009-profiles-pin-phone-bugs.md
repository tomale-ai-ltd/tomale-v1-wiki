---
date: 2026-11-18
source: cursor
branch: 009-profiles-pin
feature: 009-profiles-pin
---

# Four phone-pass bugs committed, not pushed

## What changed
- `7f7a2bf` Fit the PIN keypad, including Forgot PIN, on a tall phone. Keys stay in three columns and shrink to the space above the link. Change PIN's current step has the link too, and it opens the forgot screen.
- `56a36b9` Skip the profile picker when the account has no children. Cold start always loads the profile list before deciding. A sign-out clears the saved list. PIN state is not part of the decision.
- `6fedab0` Draw each profile's character picture instead of the bear. One household character fetch, looked up by id, passed into the header, picker, pad, Manage, avatar menu, and the edit preview. PATCH still sends `character:<id>`. Archived, deleted, and not-ready pictures stay on the bear.
- `e7d96c9` Let a parent edit their own profile. The primary row opens Edit. Delete stays hidden for the primary profile.

## Decisions
- Kyle reported these from the iPhone 17 Pro Max pass. Snags from the earlier screenshot pass were left alone.
- Cursor did not start or stop Metro or the simulator, and did not take screenshots.

## Open questions / blockers
- Kyle still needs to confirm these four on the handset. T034 is still open.

## Next
- Kyle's handset check of the keypad, a no-children account, a character picture, and Edit on the parent row.
