---
type: plan-task
id: IP-11
title: "Shadow mode for a week"
status: todo
owner: "Cursor + Kyle"
depends:
  - "[[IP-10-xano-session-a]]"
gate: ""
effort_days: 0.5
target: 2026-12-24
scoping: test-plan
project: tomale-rn-v1
---

# IP-11: Shadow mode for a week

**Goal:** Gateway records run on test stories in parallel (outputs to a `shadow/` prefix, never shown) while OpenAI stays default; compare with the harness.

**Done when:** Eval parity holds on live data; no callback or lease errors.

**Notes:** Needs a per-story switch in the executor or test-only default switching; settle in the Session A brief.

Plan: [[image-pipeline-plan]] · Scope: [[PRD-Image-Pipeline]]
