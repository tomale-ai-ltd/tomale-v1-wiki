# 009 profiles and PIN: mock-up source

Exported 18/11 from the Claude Design canvas "Tomale Profiles and PIN screens (009)" (private to Kyle's account). Each `.dc.html` file is one 390-wide phone screen. The markup's inline styles are the exact values; map them to theme tokens. `data-props` at the bottom of each file lists the states (the tweaks), and `renderVals()` shows what changes in each state.

| Board | File | States (`data-props`) |
|---|---|---|
| 901 Avatar menu | `Main.dc.html` | `profile`: parent, child |
| 902 Profile picker | `ProfilePicker.dc.html` | — |
| 903 PIN pad | `PinPad.dc.html` | `state`: entering, correct, wrong |
| 904 PIN locked / Forgot PIN | `PinLocked.dc.html` | `state`: locked, forgot, sent, just-sent |
| 905 Set PIN | `SetPin.dc.html` | `step`: first-child, confirm, mismatch, change-current |
| 906 Manage profiles | `ManageProfiles.dc.html` | — |
| 907 Add / edit profile | `EditProfile.dc.html` | `mode`: add, edit · `avatarTab`: pictures, characters, characters-empty · `nameState`: default, empty, rejected · `typedName` · `pictureChosen` |
| 908 Delete confirmation | `DeleteProfile.dc.html` | — |
| Avatar set | `AvatarSet.dc.html` | 30 animals; the shipped SVGs are in `Project/Design/avatars/` |

Notes:
- `<dc-import name="Art" kind="…">` is placeholder character art (bear, girl, fox, dragon, robot, pending). In the app, profile avatars come from `avatar_key` and characters from their pictures.
- The preset tiles on 907 are placeholders; the real picker uses the 30 animal avatars (RS-2026-11-18-01).
- Fonts: Glacial Indifference (already in the app). Header bands follow RS-2026-11-17-03 (kit `ScreenHeader`, under the status bar).
- Behaviour that isn't drawn is in the micro-PRD's "Design notes".
- PNG screenshots: Kyle exports them from the canvas into this folder if Cursor needs pixel references.
