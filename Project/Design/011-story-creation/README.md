# 011 make a story: mock-up source

Drawn 24/11 on the Claude Design canvas "Tomale Make a story screens (011)" (https://claude.ai/artifact/8xGVeLeKT7UnjCJ8pZUJf6, private to Kyle's account). Each `.dc.html` file is one 390-wide phone screen. Inline styles are the exact values; map them to theme tokens. `data-props` at the bottom of each file lists the states (the tweaks), and `renderVals()` shows what changes in each state. Behaviour that isn't drawn is in the micro-PRD (`.docs/prd/011-story-creation.md`).

| Board | File | States (`data-props`) |
|---|---|---|
| 1101 Create · Being made and Story builder | `Main.dc.html` | `empty` |
| 1102 Story chat | `Chat.dc.html` | `step`: characters, theme, style, idea, ideas, phonics, summary · `profile`: parent, child (allowance line) |
| 1103 Being made | `Making.dc.html` | `stage`: writing, pictures |
| 1104–1105 Home · being-made card and ready toast | `HomeMaking.dc.html` | `profile`: parent, child · `toast`: none, ready, ready-held |
| 1106 Story cover (until 012) | `Cover.dc.html` | `phonics` |
| 1107 Limit reached | `Limit.dc.html` | `profile`: child, parent |
| 1108 Couldn't make it | `Problem.dc.html` | `kind`: blocked, failed |

Notes:
- `<dc-import name="Art" kind="…">` is placeholder art (bear, girl, fox, dragon, robot). In the app: character pictures from the character, covers from the story, avatars from `avatar_key`.
- Art-style cards use coloured blocks as stand-ins: in the app each shows the style's `sample_image`.
- Chat shows only the last answered step above the current question to keep the board short; in the app the whole conversation so far scrolls above.
- Header bands, the BackButton (48 × 48 white circle) and toasts follow 009/010/010b.
- Grey blocks behind sheets are stand-ins: in the app the real screen stays visible under a 40% `ink` scrim, no blur.
