---
type: plan-task
id: IP-06
title: "Evaluation harness and rating sheet"
status: todo
owner: "Cursor"
depends:
  - "[[IP-05-golden-set]]"
  - "[[IP-04-spec-contract-and-repo]]"
gate: ""
effort_days: 3
target: 2026-12-08
scoping: full-spec
project: tomale-rn-v1
---

# IP-06: Evaluation harness and rating sheet

**Goal:** Python harness: character detection crops, DINOv2/CLIP drift scores, VLM judge (attributes from the JSON model, which-reference bleed check, guideline check), Character-F1 and Frame-Accuracy; blind rating sheet for Kyle and 2–3 parents; runs in CI on prompt or model change.

**Done when:** Reproduces a baseline on today's OpenAI outputs; judge agreement spot-checked by Kyle on 20 pages.

**Notes:** Decision: [[measure-character-consistency-with-a-vlm-judge-and-blind-ratings]].

Plan: [[image-pipeline-plan]] · Scope: [[PRD-Image-Pipeline]]
