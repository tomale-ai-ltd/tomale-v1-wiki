---
type: plan-task
id: IP-12
title: "Load test: 20 books at once"
status: todo
owner: "Cursor"
depends:
  - "[[IP-10-xano-session-a]]"
gate: "G2"
effort_days: 1
target: 2026-12-22
scoping: test-plan
project: tomale-rn-v1
---

# IP-12: Load test: 20 books at once

**Goal:** Queue 20 test books together; tune the Cloud Tasks rate and concurrency caps to Vertex's dynamic quota.

**Done when:** p95 book time under 3 minutes; zero lost or duplicate jobs; 429s absorbed.

Plan: [[image-pipeline-plan]] · Scope: [[PRD-Image-Pipeline]]
