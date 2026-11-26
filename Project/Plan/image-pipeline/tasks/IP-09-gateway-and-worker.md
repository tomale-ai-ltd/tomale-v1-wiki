---
type: plan-task
id: IP-09
title: "Gateway and worker service"
status: todo
owner: "Cursor"
depends:
  - "[[IP-04-spec-contract-and-repo]]"
  - "[[IP-08-terraform]]"
gate: ""
effort_days: 4
target: 2026-12-12
scoping: full-spec
project: tomale-rn-v1
---

# IP-09: Gateway and worker service

**Goal:** Provider adapters (Gemini, OpenAI) keyed by `model_settings`; compiler call; reference assembly with labels and the 4-character cap; moderation layers; S3 put; callback with retries and HMAC; idempotency by job id and attempt; kill switch; structured logs with cost per job.

**Done when:** Unit and integration tests green; contract tests against a Xano mock; runs end to end in dev against the golden set.

**Notes:** Uses the setup chosen at G1 (adapter config, so it can start before G1 ends).

Plan: [[image-pipeline-plan]] · Scope: [[PRD-Image-Pipeline]]
