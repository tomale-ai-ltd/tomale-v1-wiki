---
type: brief
title: ip-04-cursor-brief
project: tomale-rn-v1
status: draft
date: 2026-11-26
related:
  - "[[IP-04-spec-contract-and-repo]]"
  - "[[PRD-Image-Pipeline]]"
  - "[[build-image-infrastructure-in-a-cursor-terraform-repo]]"
---

# IP-04: gateway repo foundation, spec and contract (Cursor brief)

Two PRs into `main` of `tomale-ai-ltd/tomale-image-gateway` (cloned at `~/Developer/tomale/tomale-image-gateway`). **No service code, no Terraform, no cloud or Xano calls** in IP-04. That's IP-08 and IP-09, specified after Kyle approves this contract.

## Read first

All in the `tomale-v1-wiki` folder of the workspace:
- `Canonical/prd/PRD-Image-Pipeline.md`: scope, requirements R1–R11 / N1–N2 / C1–C6, gates.
- `Canonical/architecture/image-pipeline-future-state.md`: the target flow and the 13-image sequence.
- `Project/Research/Image Pipeline/image-pipeline-research-2026-11.md`: models, regions, limits, costs.
- The nine image-pipeline decision notes listed in PRD §9 (in `Project/Decisions/`).
- `Project/Plan/image-pipeline/golden-set/README.md` and `tasks/IP-02-child-image-policy-spike.md` (G0 findings).
- `Canonical/architecture/image-generation-flow.md` and `Canonical/backend-xano.md`: today's Xano pipeline and its rules.
- `Repos/tomale-xano/function/ai_pipeline_executor_page_image.xs`, `ai_pipeline_image_worker_tick.xs`, `ai_pipeline_claim_image_jobs.xs`: what the contract has to fit. Read-only.
- `tomale-rn-test/.cursor/` (permissions, hooks, rules) and `tomale-rn-test/.github/workflows/ci.yaml`: the guard rails and CI to copy.

---

## PR A: repo foundation (`chore/foundation`)

Prompt for Cursor:

> In `tomale-image-gateway`, on branch `chore/foundation`, set up the repo foundation. One commit per bullet.
> - **Guard rails:** copy `.cursor/permissions.json`, `.cursor/hooks.json` and `.cursor/hooks/guard.sh` from `tomale-rn-test`, then extend the guard:
>   - **deny:** `terraform apply` and `destroy` (any flags), `terraform import`/`state` writes, any `gcloud`/`gsutil`/`bq` command except `--help` and read-only `describe`/`list`/`get`, and any `aws` command except `sts get-caller-identity` and read-only `describe`/`list`/`get`.
>   - **ask:** `terraform plan`, `terraform init`.
>   - Keep every existing rule (no merges, force pushes, pushes to `main`, or remote branch deletes).
>   Add tests for the new guard rules in the same style as rn-test, if it has them; otherwise a small `tests/guard/` script with allow/deny cases.
> - **Project rule:** `.cursor/rules/tomale-gateway.mdc`, short, always applied. The vault PRD and decisions are the source of scope. Contract-first: no endpoint or payload change without updating `contracts/`. Never hold or print cloud credentials or API keys. No real child photos anywhere. EU processing (`eu` Vertex endpoint, AWS eu-west-2). Raw session note to `tomale-v1-wiki/_raw/Chat Sessions/` at the end, in the Cursor format.
> - **Spec Kit: copy, don't install.** Copy `.specify/templates/`, `.specify/scripts/` and `.cursor/commands/speckit.*` from `tomale-rn-test` unchanged, so both repos run the same Spec Kit (installed October 2025; the current release uses different commands). Don't copy `.specify/memory/constitution.md` (written below) or `.cursor/rules/specify-rules.mdc` (the plan step regenerates it). Record in the README that the copy comes from rn-test at its current commit and is upgraded with rn-test after launch. Don't edit these files afterwards.
> - **Constitution:** apply the text of `tomale-v1-wiki/Project/Plan/image-pipeline/gateway-constitution-draft.md` below the horizontal rule **verbatim** with `/speckit.constitution` (version 1.0.0), adding only the Sync Impact Report comment. Don't reword it; raise any conflict with the templates as a question instead.
> - **Tooling:** Python 3.13 with `uv` (`pyproject.toml`), `ruff`, `pytest`; `.gitignore` for Python, Terraform, `.env*` and `eval/output/`; `README.md` (what the repo is, the links above, how to run tests); `.editorconfig`.
> - **CI:** `.github/workflows/ci.yaml` with one job named `test`: Gitleaks, ruff, pytest (guard tests), and an OpenAPI lint (Redocly or Spectral) that skips if there's no contract yet. checkov and tflint arrive with IP-08.
> Open a PR and confirm `test` is green with `gh pr checks` before reporting it ready. Don't merge.

**Kyle, after merge:** add `test` as a required status check in the `protect-main` ruleset.

---

## PR B: spec, contract, ADRs, threat model (`001-image-gateway`)

Prompt for Cursor:

> Create `.docs/prd/001-image-gateway-micro-prd.md` from `Canonical/prd/PRD-Image-Pipeline.md`: scope for this repo only, with requirements and gates kept and their ids preserved. Then run `/speckit.specify` (referencing the micro-PRD) → `/speckit.clarify` → `/speckit.plan` → `/speckit.analyze`. **Stop there.** No `/speckit.tasks` or `/speckit.implement` until Kyle approves the contract.
>
> **The plan must produce `contracts/gateway.openapi.yaml` (OpenAPI 3.1) covering:**
> 1. **`POST /v1/batches`** (Xano → gateway).
>    - **Auth:** HMAC-SHA256 over `timestamp + "." + raw body` in `X-Tomale-Signature`, plus `X-Tomale-Timestamp`, a 5-minute replay window, and the secret in Secret Manager.
>    - **Body:** `batch_id`, `instant_stories_id` (nullable for character jobs), `callback_url`, and `jobs[]` (max 20). Each job has:
>      - `image_jobs_id`, `attempt`, `job_type` (`cover-image` | `page-image` | `character-image`)
>      - `data_model`: id, slug, version, and a snapshot of `model_settings`
>      - `inputs`: page text and number, synopsis, title and subtitle for the cover, `characters[]` with the full attribute JSON and a `reference_image_url` (nullable), `artwork_style` (description, positive/negative prompts, `sample_image_url`), and `theme` (name, keywords)
>      - `instruction` (nullable, character "draw again", already moderated by Xano)
>      - `use_reference`
>    - **Response:** `202` with `accepted[]` and `rejected[]` (`{image_jobs_id, code, message}`). A duplicate `image_jobs_id` + `attempt` is accepted with `duplicate: true`. `401` bad signature, `400` validation, `503` kill switch on.
> 2. **Callback** (gateway → Xano `webhooks` group), as an OpenAPI `webhooks` entry. Same HMAC scheme. Body:
>    - `image_jobs_id`, `attempt`, `status` (`complete` | `error_retry` | `error_terminal`)
>    - `storage`: `s3_key`, width, height, mime
>    - `provider`, `model`, `usage` (input/output tokens, `estimated_cost_usd`)
>    - `moderation`: `enforcement` using Tomale's values `none` | `require_parental_oversight` | `blocked` | `flag_account`, `provider_codes[]`, `rekognition_labels[]`, `judge` summary
>    - `timings`; `error`: `code`, `message`, `retryable`
>    Xano must be able to upsert it idempotently. Keep it small: no prompts, no image bytes.
> 3. **`GET /v1/health`.**
> 4. **A shared error-code list:** `INVALID_SIGNATURE`, `STALE_TIMESTAMP`, `VALIDATION_FAILED`, `TOO_MANY_CHARACTERS` (over 4 referenced), `KILL_SWITCH`, `PROVIDER_RATE_LIMITED`, `PROVIDER_SAFETY_BLOCK`, `MODERATION_BLOCKED`, `STORAGE_FAILED`, `CALLBACK_FAILED`, `INTERNAL`.
>
> **Also in the plan:**
> - **ADRs:** in `docs/adr/`, one per vault decision note in PRD §9, linking back to it by vault path.
> - **Threat model:** `docs/threat-model.md`, STRIDE over the batch endpoint, callback, cross-cloud identity (Cloud Run → AWS STS), S3 and CloudFront, prompt injection through user text into image prompts, moderation bypass, cost exhaustion (abuse, retry storms), and children's data.
> - **Xano feasibility:** `docs/xano-feasibility.md`, listing every assumption the contract makes about Xano for Kyle to confirm: computing HMAC-SHA256 in XanoScript, raw-body access on a webhook endpoint, request size limits, and timeouts on the outbound batch call. **Don't guess. List them as open questions.**
> - **Mapping:** `docs/mapping.md`, from each contract field to the Xano table and field it comes from or writes to (`image_jobs`, `instant_story_pages`, `instant_stories`, `characters`, `token_usage`, `executor_runs`, `data_models`).
>
> Open a PR with CI green (OpenAPI lint must pass). Don't merge. Write the raw session note.

**Kyle reviews PR B:** the contract, the Xano feasibility questions and the threat model. Claude checks the contract against the Xano mirror before Kyle approves. After approval, IP-08 (Terraform) and IP-09 (gateway and worker) are briefed.
