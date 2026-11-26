---
type: plan
title: gateway-constitution-draft
project: tomale-rn-v1
status: approved
date: 2026-11-26
related:
  - "[[ip-04-cursor-brief]]"
  - "[[PRD-Image-Pipeline]]"
---

# Draft: tomale-image-gateway constitution 1.0.0

For Kyle to approve (26/11: three details from Cursor's first version folded in: cost fields on failed jobs, no vendor SDK outside adapters, guard tests). Once it's approved, Cursor applies the text below the line **verbatim** with `/speckit.constitution` in PR A, adding only the Sync Impact Report comment at the top. Later changes follow the Governance section, as in rn-test.

---

# Tomale Image Gateway Constitution

## Core Principles

### 1. Children's Safety and Privacy (NON-NEGOTIABLE)
- Every generated image MUST pass output moderation (provider safety filters, Amazon Rekognition and the Tomale guideline judge) before its result is reported as `complete`. Results MUST map to Tomale's enforcement values (`none`, `require_parental_oversight`, `blocked`, `flag_account`).
- The gateway MUST NOT accept, store or forward photographs of real people. Reference images are generated character pictures only.
- ML processing MUST stay in the EU: Vertex AI `eu` endpoint, AWS `eu-west-2`. A provider or endpoint outside the EU needs a documented decision and a DPIA update first.
- Logs, traces and callbacks MUST contain only ids, statuses, timings, sizes and costs: never prompts, page text, character attributes or image bytes.
- Images MUST be stored privately (S3 Block Public Access, encryption at rest) and served only through short-lived signed URLs.
Rationale: the users are families and the characters are often modelled on their children.

### 2. Contract-First Integration with Xano
- `contracts/gateway.openapi.yaml` is the single source of truth for the batch endpoint and the Xano callback. Code, tests and Xano changes follow the contract, never the reverse.
- Any change to the contract MUST be versioned, reviewed by Kyle, and released together with the matching Xano change. Breaking changes need a new version path.
- `image_jobs` in Xano remains the system of record for job state. The gateway never decides that a story is complete.
Rationale: Xano is changed by hand by one person, so the interface must be explicit and stable.

### 3. Fail Closed, Converge, Be Idempotent
- Every accepted job MUST end in exactly one terminal callback (`complete` or `error_terminal`) or be safely retried. If the callback can't be delivered, Xano's lease reaper requeues the job. No path may silently drop a job.
- `image_jobs_id` + `attempt` is the idempotency key for enqueueing, generation, storage keys and callbacks. A duplicate delivery MUST NOT cause a second paid generation or a second write.
- Unknown values, missing fields and failed signature checks MUST be rejected, not defaulted.
- A kill switch MUST stop new work without losing queued jobs.
Rationale: duplicate paid generations and stuck jobs were Phase 1's worst bugs.

### 4. Security by Default
- No long-lived credentials: people use Application Default Credentials, CI and services use Workload Identity Federation, and Cloud Run reaches AWS through OIDC web-identity federation. Service account keys and AWS access keys MUST NOT be created.
- Secrets live in Secret Manager or AWS Secrets Manager, never in the repo, environment files or logs.
- Least privilege: each identity gets only the roles it uses, reviewed with IAM Access Analyzer before go-live.
- Every request between Xano and the gateway MUST carry an HMAC-SHA256 signature with a timestamp and a 5-minute replay window.
Rationale: one founder holds the keys to two clouds and a children's dataset.

### 5. Evaluation-Gated Model Changes
- Changing a provider, model, prompt template or reference strategy MUST be backed by a golden-set evaluation run (VLM attribute and bleed judge, drift metrics) with results stored alongside the change.
- Going live with a new default needs blind human ratings at least as good as the current baseline, and a bleed rate no higher.
- Providers sit behind adapters keyed by `data_models.model_settings.provider` and `model`, so a model can be swapped by configuration and rolled back by switching the Xano default. Code outside the adapter layer MUST NOT call a vendor SDK directly.
Rationale: consistency without attribute bleed is the product's core promise, and models change every few months.

### 6. Cost and Credit Awareness
- Every callback MUST report provider, model, token usage and estimated cost, which Xano records in `token_usage`. This includes failed jobs whenever any provider call was made.
- Budgets with alerts at 25/50/75% MUST exist on both clouds, tracking spend before credits.
- Concurrency and rate caps MUST protect against retry storms and quota exhaustion. Nothing may scale without a ceiling.
- Idle infrastructure MUST scale to zero.
Rationale: credits are finite and expire on 30/06/2027, and costs after that are paid from revenue.

## Additional Constraints & Technology Standards

- **Runtime:** Python 3.13, managed with `uv`; `ruff` for lint and format; `pytest` for tests; type hints on all public functions.
- **SDKs:** `google-genai` for Vertex AI (`enterprise=True`, `location="eu"`); `boto3` for AWS. Versions are pinned and updated deliberately.
- **Compute:** Cloud Run (gateway and worker) and Cloud Tasks in `europe-west2`; Lambda (URL signer) in `eu-west-2`.
- **Storage:** S3 `eu-west-2` behind CloudFront with Origin Access Control; 1-hour signed URLs.
- **Infrastructure:** Terraform only, with google and aws providers, dev and prod workspaces, checkov and tflint clean. `terraform apply` is run by Kyle only.
- **Observability:** structured JSON logs with `image_jobs_id`, `attempt`, `provider`, `model`, latency, cost and moderation verdict; Cloud Monitoring and CloudWatch alerts on error rate, 429 rate and book p95 time.
- **Limits:** at most 4 referenced characters per image; at most 20 jobs per batch.

## Development Workflow & Quality Gates

- **Constitution Check gate:** every plan MUST confirm alignment with Principles 1–6, with explicit notes on moderation and privacy, contract impact, idempotency, credentials, evaluation evidence and cost.
- **Contract gate:** a plan that touches the interface MUST update `contracts/` first; the OpenAPI lint and contract tests MUST pass.
- **Spec-driven:** `/speckit.specify` → `/speckit.clarify` → `/speckit.plan` → `/speckit.analyze` → `/speckit.tasks` → `/speckit.implement`, one numbered feature per branch, from a micro-PRD in `.docs/prd/`.
- **CI gate:** the `test` job (Gitleaks, ruff, pytest, OpenAPI lint, plus checkov, tflint and `terraform plan` once Terraform exists) MUST pass before merge.
- **Branch protection:** no direct pushes to `main`; all changes by PR; linear history; Kyle merges.
- **Agent guard rails:** `.cursor/permissions.json` and `guard.sh` MUST block `terraform apply`/`destroy`, changes to cloud resources, merges and pushes to `main` from agents. The guard tests in `tests/guard/` MUST stay green.
- **Documentation:** ADRs in `docs/adr/` mirror the vault decision notes; the README links to the vault PRD; each session ends with a raw note in the vault.

## Governance

- **Authority:** this constitution governs engineering in `tomale-image-gateway` and supersedes other practices where they conflict. Scope and decisions come from the `tomale-v1-wiki` vault (PRD-Image-Pipeline and its decision notes).
- **Amendments:** by PR updating this file with a Sync Impact Report. Kyle, as document owner, MUST approve explicitly.
- **Versioning:** semantic versioning. MAJOR for a removed or redefined principle; MINOR for a new principle or section, or materially expanded guidance; PATCH for clarifications.
- **Exceptions:** documented in the plan with scope, rationale and a sunset date.
