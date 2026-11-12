---
date: 2026-11-12
source: cursor
branch: 008-characters
feature: 008-characters
---

# Create form pushed; Draw again up for review

## What changed
- `bdc208b` restyles the new-character form: 20 px between field groups and under the intro line, 8 px between the picture and that line, and the artboard's soft yellow circle as the `highlight-soft` token. Pushed to `origin/008-characters`. No pull request. Shots are in `.screenshots/create/`.
- Draw again is restyled to `DrawAgain.dc.html`, including refused-instruction, already-drawing, and saving. Not committed. Shots are in `.screenshots/draw-again/`.

## Decisions
- Kyle approved the create form after the spacing fix, and asked for the soft circle.
- The refused-instruction preview uses the artboard sentence "We can't draw characters from films or books. Try describing your own idea instead." A real refusal still shows the server's message. Already-drawing uses "[Name] is already being drawn." and "Try again in a few minutes." Saving keeps the label "Draw again" with a spinner, and the button dims.
- The refused-description preview on the create form still uses the kit sentence "That description isn't allowed. Please try another." A real refusal shows the server's message.

## Open questions / blockers
- Kyle's review of Draw again, including whether the film-or-book sentence stays.

## Next
- Kyle reviews `.screenshots/draw-again/`. Do not commit Draw again until he asks. After that, the delete confirmation.
