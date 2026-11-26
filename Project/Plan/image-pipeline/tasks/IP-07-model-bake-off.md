---
type: plan-task
id: IP-07
title: "G1: model and reference bake-off"
status: todo
owner: "Cursor, Kyle rates"
depends:
  - "[[IP-06-eval-harness]]"
  - "[[IP-02-child-image-policy-spike]]"
gate: "G1"
effort_days: 2
target: 2026-12-12
scoping: test-plan
project: tomale-rn-v1
---

# IP-07: G1: model and reference bake-off

**Goal:** Compare Flash Image `eu`, Nano Banana 2.1 global, Gemini 3 Pro Image and gpt-image-2.6 on the golden set; reference strategies: labelled portraits, character sheets, style reference, 1K vs 2K; also 20 in-scene text prompts.

**Done when:** G1: chosen setup ≥ baseline on blind consistency, bleed ≤ baseline, VLM attribute accuracy ≥ 90%. Then accept or amend [[use-gemini-3-1-flash-image-on-vertex-eu-for-story-images]].

**Notes:** About $50–150 of credit.

Plan: [[image-pipeline-plan]] · Scope: [[PRD-Image-Pipeline]]
