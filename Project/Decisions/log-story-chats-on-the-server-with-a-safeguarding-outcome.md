---
type: decision
title: "log-story-chats-on-the-server-with-a-safeguarding-outcome"
project: tomale-rn-v1
status: accepted
date: "2026-11-26"
related:
  - "[[2026-11-26-001]]"
  - "[[011-story-creation-micro-prd]]"
  - "[[011-xano-prompts]]"
  - "[[PU-2026-11-26-01]]"
  - "[[moderate-free-text-instructions-with-moderation-text-policy]]"
affects:
  - "[[PRD-Chatbot-Story-Conversations]]"
  - "[[roadmap]]"
  - "[[pre-launch-checklist]]"
  - "[[backend-xano]]"
  - "[[content-moderation-policy-v1.0]]"
  - constitution
  - conversations
  - moderation_flags
features:
  - F-story-chatbot
  - F-story-generation
  - X-security
---

# Decision: log-story-chats-on-the-server-with-a-safeguarding-outcome

## What we decided

Kyle, 26/11: store a server-written conversation log per story, moderate the story idea when it is confirmed, add a safeguarding outcome for possible disclosures (safe message, no automatic parent alert, internal review), and count moderation strikes. This replaces the 24/11 scoping line "no stored transcript in V1" ([[PRD-Chatbot-Story-Conversations]] 2.1).

## Why

So chats reload with their history and the log can serve as evidence. It came from Kyle's questions on audit and duty of care: 011 adds a free-text idea box used by children, and moderation treated self-harm and abuse as ordinary content, so a child disclosing harm would have seen "try a different idea" ([[PU-2026-11-26-01]]).

## Alternatives considered

The 24/11 scope: no stored transcript, with the chat rebuilt from the draft's fields and `conversations` not used for stories in V1.

## Trade-offs accepted

Adds about two days to 011. Not otherwise discussed in session notes.

## Workflow detail

As worked into [[011-story-creation-micro-prd]] and [[011-xano-prompts]] (X1–X12) on 26/11:
- Opening the chat creates the draft and its `conversations` row (story type). Every story endpoint appends an event (idea versions, AI ideas and suggestions, Surprise me picks, choices, moderation outcomes, "Make my story"); the app never writes the log. Resuming renders the chat from `GET /instant_stories/{id}/conversation`, which returns display-only events, never moderation or safeguarding details.
- Confirming the idea (`POST /instant_stories/{id}/idea`) moderates it; `CONTENT_REJECTED` keeps the person at step 1 with a Tomale bubble, `SAFEGUARDING_CONCERN` opens the safe-message sheet (board 1109). A story blocked for a safeguarding reason shows 1109, with `blocked_kind` "content" or "safeguarding" and never the reason.
- Strikes: 3 refusals in 30 days → `flag_account`, reviewed by Tomale; no automatic account lock in 011.
- What must be true before launch (safeguarding advice, runbook, evidence retention, purge exemption, Online Safety Act re-check) is in [[PU-2026-11-26-01]].

## Related notes

[[2026-11-26-001]], [[011-story-creation-micro-prd]], [[011-xano-prompts]], [[PU-2026-11-26-01]], [[PRD-Chatbot-Story-Conversations]], [[content-moderation-policy-v1.0]], [[moderate-free-text-instructions-with-moderation-text-policy]]
