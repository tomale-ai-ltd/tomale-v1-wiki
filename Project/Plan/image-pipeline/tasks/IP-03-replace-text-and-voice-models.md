---
type: plan-task
id: IP-03
title: "Replace gpt-4o-mini (14/01) and gpt-4o-mini-tts (6/01)"
status: todo
owner: "Kyle + Claude chat"
depends:
  - "[[IP-00-xano-session-0]]"
gate: ""
effort_days: 1.5
target: 2026-12-17
scoping: test-plan
project: tomale-rn-v1
---

# IP-03: Replace gpt-4o-mini (14/01) and gpt-4o-mini-tts (6/01)

**Goal:** Choose replacements for Xano's own text calls (moderation-name, moderation-text, story text, story chat, generate_character_model) and read-aloud TTS: OpenAI (`gpt-6-luna`; TTS replacement named `gpt-realtime-2.1-mini`, check it serves `/v1/audio/speech`) or credit-funded Google (Gemini Flash-Lite; Cloud Text-to-Speech). Then switch the records and hard-coded model names.

**Done when:** No call to a model with a shutdown date before 30/06/2027. Postman folders 2, 5, 7 and the moderation cases (5A-2, 5D copyright) green. One story read aloud checked by ear.

**Notes:** Moderation behaviour can shift with a new model, so rerun the red-team prompts. Best done inside Session A. Not strictly image pipeline, but launch-critical and found by this research.

Plan: [[image-pipeline-plan]] · Scope: [[PRD-Image-Pipeline]]
