---
session-name: "2026-11-26-claude-011-safeguarding"
type: session-note
project: tomale-rn-v1
date: 2026-11-26
tags: [011, story-creation, safeguarding, moderation, conversations]
---

# Work Session (Claude chat, 26/11)

## What I actually did
- Folded Kyle's scope edits into the 011 micro-PRD (idea first; characters and theme suggested from the idea; Surprise me; chat look; animated progress, ready toast and pull-to-refresh; phonics section). Revised the canvas (boards 1101–1106) and the vault export. Applied PU-2026-11-24-13 (PRD 2.1).
- Then, after Kyle's questions on audit and duty of care: reworked the micro-PRD and `011-xano-prompts.md` (now X1–X12) for a server-written conversation log, moderation when the idea is confirmed, a `safeguarding_concern` outcome and strikes. Added board 1109 (safe message) and a refused-idea chat state. Drafted PU-2026-11-26-01 (safeguarding and evidence before launch).

## Decisions made
- Kyle, 26/11: story chat order is idea first, then characters, theme, style, phonics, summary.
- Kyle, 26/11: characters pre-ticked from names in the idea plus one AI suggestion call; a shared name ticks only the most recently made character.
- Kyle, 26/11: "Surprise me" picks idea, characters and theme from the profile's past stories, then shows the summary.
- Kyle, 26/11: pull-to-refresh on Home, Create and story lists, with a pull, hang and rebound animation.
- Kyle, 26/11: chat background is cream with faint brand shapes; Tomale bubbles grey on the left, the person's replies coral on the right with their avatar.
- Kyle, 26/11: store a server-written conversation log per story (so chats reload with their history and can serve as evidence), moderate the idea when it's confirmed, add a safeguarding outcome for possible disclosures (safe message, no automatic parent alert, internal review), and count moderation strikes. Adds about two days to 011.

## Next session
- Kyle approves PU-2026-11-26-01; reviews the reworked Xano prompts (X1–X12); starts with X1–X4.
