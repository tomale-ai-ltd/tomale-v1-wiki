---
type: plan-task
id: IP-04
title: "Spec, contract, ADRs, threat model and repo"
status: in-progress
owner: "Cursor"
depends:
  - "[[IP-02-child-image-policy-spike]]"
gate: ""
effort_days: 1.5
target: 2026-12-02
scoping: full-spec
project: tomale-rn-v1
---

# IP-04: Spec, contract, ADRs, threat model and repo

**Goal:** Create `tomale-image-gateway` (Tomale.ai Ltd org, branch protection, required CI); `.cursor/rules` and guard rails copied from rn-test, with cloud rules added; spec (from [[PRD-Image-Pipeline]]); OpenAPI contract for `POST /v1/batches` and the Xano callback (payload, HMAC, idempotency key, error codes); ADRs mirroring the decision notes; STRIDE threat model; moderation thresholds.

**Done when:** Kyle reviews and approves the spec and contract; the vault links the repo (PU-2026-11-24-08).

**Notes:** The contract is the one hard interface with Xano, so it's specified fully before IP-09 or IP-10 start.

Plan: [[image-pipeline-plan]] · Scope: [[PRD-Image-Pipeline]]

**Brief:** [[ip-04-cursor-brief]] (26/11): PR A foundation, then PR B spec and contract (stops before `/speckit.tasks`).
- **26/11:** PR A (#1, `chore/foundation`) ready to merge at `18fb995`: guard rails with position-aware, fail-closed cloud rules and secret-read denies (62 guard tests; Claude spot-checked 34 cases), gateway rule, Spec Kit copied from rn-test `@05f27b1`, constitution 1.0.0 (the approved draft, verbatim), uv tooling, CI `test` green. Next: merge, make `test` required, the guard check in the workspace, then PR B.
