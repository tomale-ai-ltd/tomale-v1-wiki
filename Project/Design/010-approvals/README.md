# 010 approvals: mock-up source

Exported 18/11 from the Claude Design canvas "Tomale Approvals screens (010)" (private to Kyle's account). Each `.dc.html` file is one 390-wide phone screen. Inline styles are the exact values; map them to theme tokens. `data-props` at the bottom of each file lists the states (the tweaks), and `renderVals()` shows what changes in each state. Behaviour that isn't drawn is in the micro-PRD's "Design notes" (`.docs/prd/010-approvals.md`).

| Board | File | States (`data-props`) |
|---|---|---|
| 1001 Home · parent (minimal) | `Main.dc.html` | `reviewCount`: 0, 1, 2 |
| 1002 Home · child | `HomeChild.dc.html` | `tapped`: waiting sheet shown |
| 1003 Avatar menu · parent with Approvals | `AvatarMenu.dc.html` | — |
| 1004 Approvals inbox | `Inbox.dc.html` | `tab`: review, rejected · `empty` · `toast`: none, approved, approved-not-ready, rejected |
| 1005 Review story | `Review.dc.html` | `story`: text-ready, text-pending · `page`: 1–4 |
| 1006 Reject confirmation | `RejectSheet.dc.html` | — |
| 1007 Rejected story actions | `RejectedActions.dc.html` | `step`: actions, confirm-delete |

Notes:
- `<dc-import name="Art" kind="…">` is placeholder art (bear, girl, fox, dragon, robot, pending). In the app: profile avatars from `avatar_key` (009), story covers from the story, character pictures from the character.
- Header bands use the kit `ScreenHeader` from 009 (under the status bar, no fixed heights): tall on Home, compact elsewhere.
- Grey blocks behind sheets are stand-ins: in the app the real screen stays visible under a 40% `ink` scrim, no blur.
- Quick actions and "Favourite stories" / "My favourites" are placeholders (see the micro-PRD): "New character" opens the 008 form; "New story" is "Coming soon" until 011; favourites stay empty.
- The "Minimal Home for 010…" line on 1001 is a design note, not app copy.
- PNG screenshots: Kyle exports them from the canvas into this folder if pixel references are needed.
