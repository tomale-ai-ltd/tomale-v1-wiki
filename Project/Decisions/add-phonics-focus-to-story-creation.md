---
type: decision
title: add-phonics-focus-to-story-creation
project: tomale-rn-v1
status: accepted
date: 2026-10-29
related:
  - "[[PRD-Chatbot-Story-Conversations]]"
  - "[[v2-backlog]]"
affects:
  - instant_stories
  - data_models
  - "[[PRD-Chatbot-Story-Conversations]]"
features:
  - F-phonics
  - F-story-chatbot
  - F-story-generation
---

# Decision: add-phonics-focus-to-story-creation

## What we decided

V1 story creation gets an **optional phonics focus**. The user picks a scheme, phase and stage from suggestion cards in the story chat. Generation then loads the graphemes and tricky words up to that stage (existing functions) and adds them to the user prompt of the story-text model. The story stores `phonics_phase_stage_id`. There's no tracking or assessment of a child's progress, and no automated decodability check.

## Why

Kyle (29/10): the phonics data, endpoints and functions already exist, and the text model can reliably favour given graphemes and tricky words. It adds real value for parents of early readers. Tracking progress through a scheme needs architecture V1 doesn't have and would pull the product into edtech.

## Alternatives considered

- The AI picks the stage (rejected: the user chooses; the bot may only suggest).
- Leave phonics out of V1.
- Full phonics journeys with progress tracking (V2, [[v2-backlog]]).

## Trade-offs accepted

No guarantee that every word is decodable at the chosen stage; the prompt steers it. Small additions to Slice 200 (cards, one field, prompt section).

## Related notes

- [[PRD-Chatbot-Story-Conversations]]
