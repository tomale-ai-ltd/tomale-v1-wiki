---
type: decision
title: include-ai-character-creation-in-v1
project: tomale-rn-v1
status: accepted
date: 2026-10-29
related:
  - "[[PRD-Chatbot-Create-Character]]"
  - "[[roadmap]]"
  - "[[move-v1-public-launch-to-late-january]]"
affects:
  - "[[roadmap]]"
  - "[[PRD-Chatbot-Create-Character]]"
features:
  - F-character-chatbot
---

# Decision: include-ai-character-creation-in-v1

## What we decided

AI-assisted character creation (Slice 500, 501) is part of the late-January V1 launch, as milestone **M6a** after the Store (expected speckit 011). It reuses the story chat UI from M4. Voice input (502) stays behind a feature flag and is the first thing cut if the date is at risk. The Slice 100 form stays as the fallback.

## Why

Kyle (29/10): the guided chat is a more immersive experience, and the fuller character descriptions it collects should lead to better image generation, especially once character and style training arrives with the cheaper image pipeline.

## Alternatives considered

- Keep it post-launch (the roadmap's previous position), with the form covering character creation at launch.

## Trade-offs accepted

About 3–5 more working days: the estimate moves from 37–56 to 40–61 days against a late-January date. The velocity checkpoint after M2 decides whether this holds.

## Related notes

- [[PRD-Chatbot-Create-Character]]
- [[roadmap]]
