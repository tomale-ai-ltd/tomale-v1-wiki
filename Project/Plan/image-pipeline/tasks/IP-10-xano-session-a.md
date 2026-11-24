---
type: plan-task
id: IP-10
title: "Xano Session A (one sitting)"
status: todo
owner: "Kyle"
depends:
  - "[[IP-04-spec-contract-and-repo]]"
  - "[[IP-09-gateway-and-worker]]"
gate: ""
effort_days: 1.5
target: 2026-12-17
scoping: full-spec
project: tomale-rn-v1
---

# IP-10: Xano Session A (one sitting)

**Goal:** From a Claude-written brief: new gateway `data_models` records and the OpenAI fallback record; `image_jobs` status `dispatched` and storage-key fields; executor branch for `provider: tomale_gateway`; callback endpoint in `webhooks` (HMAC, idempotent upsert, story_completion_check); orchestrator dispatches the whole book; `moderation-image` record; signer call on story and character reads; env vars; IP-03 changes if decided.

**Done when:** Postman contract folder green (new folder 9); full `_tests` regression green; snapshot taken first.

**Notes:** Brief to write after IP-04, in the format of the M3 briefs.

Plan: [[image-pipeline-plan]] · Scope: [[PRD-Image-Pipeline]]
