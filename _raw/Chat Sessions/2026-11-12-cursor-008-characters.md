---
date: 2026-11-12
source: cursor
branch: 008-characters
feature: 008-characters
---

# Grid committed, then the new-character form

## What changed
- `41b48cd` restyles the character grid. A drawing tile shows "Drawing [Name]…" in the picture. Pushed to `origin/008-characters`. No pull request.
- The new-character form is restyled to `CreateCharacter.dc.html` and is not committed. Shots are in `.screenshots/create/`.

## Decisions
- Kyle approved the grid with the drawing line added in the picture.
- The refused-description preview uses the kit sentence "That description isn't allowed. Please try another." A real refusal still shows the server's message. The name refusal in the preview is the copy-sheet sentence.
- Saving shows a spinner and the label "Saving", and the button ignores another press.

## Open questions / blockers
- Kyle's review of the create form, including whether the description refusal sentence stays.

## Next
- Kyle reviews `.screenshots/create/`. Do not push again until he asks. The next screen after the form is Draw again.
