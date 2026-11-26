---
type: plan-task
id: IP-13
title: "Chaos tests"
status: todo
owner: "Cursor"
depends:
  - "[[IP-10-xano-session-a]]"
gate: "G2"
effort_days: 1
target: 2026-12-23
scoping: test-plan
project: tomale-rn-v1
---

# IP-13: Chaos tests

**Goal:** Inject 429s and 5xx, revoke the AWS role, take the Xano callback down, deliver duplicates, flip the kill switches.

**Done when:** Every job ends complete or `error_terminal`; no duplicate charges; alerts fire.

Plan: [[image-pipeline-plan]] · Scope: [[PRD-Image-Pipeline]]
