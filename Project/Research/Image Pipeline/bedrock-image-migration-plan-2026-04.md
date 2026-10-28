---
type: research
title: bedrock-image-migration-plan-2026-04
project: tomale-rn-v1
status: historical
date: 2026-04-17
owner: vault
related:
  - "[[roadmap]]"
  - "[[latent-preserving-regeneration-2026-05]]"
  - "[[image-generation-flow]]"
features:
  - F-story-generation
---

> **Imported 28/10/2026** from the Claude chat "Recreating document with project context" (17/04/2026), with the final corrections from that chat applied. It's kept as input for the image-pipeline research track ([[roadmap]] §6) and later PRDs. **It is not current.** What has changed since:
> - The image model is now `gpt-image-1.5`, not `dall-e-3`.
> - `executor_runs` now logs small status fields only ([[log-only-small-status-fields-in-executor-runs]]), and runs are found by id.
> - Credits are now £25k GCP + £10k AWS, both expiring 30/06/2027 (this plan assumed about £45k combined).
> - Check whether SDXL 1.0 is still offered on Bedrock before relying on §3 and §6.
> - Image generation is limited by entitlements at story creation, not gated by payment ([[gate-image-generation-with-entitlements-at-story-creation]]), so the PoD PRD's regeneration cap may change.
> - The worker tick runs as a background task (`image_worker_tick`); see [[image-generation-flow]].

# Tomale — R&D Implementation Plan
## AWS Bedrock Image Generation Migration

---

## 1. Overview

This document describes the implementation plan for migrating Tomale's image generation pipeline from the current OpenAI DALL-E 3 API to AWS Bedrock, using the existing `data_models` provider abstraction layer. The goal is to eliminate external rate limiting, reduce per-image cost, and establish the infrastructure foundation for future LoRA-based character consistency features.

The migration is designed as a low-risk config-record change against the existing `image_jobs` queue / `executor_runs` worker / retry architecture — not a re-architecture.

### 1.1 Objectives

- Eliminate third-party rate limiting on image generation jobs
- Reduce per-image cost using available AWS credits (~£45k across AWS and GCP)
- Maintain full compatibility with the existing `image_jobs` queue system and `executor_runs` logging
- Establish a self-controlled endpoint that supports future pipeline stages (img2img, LoRA inference)
- Validate the `data_models` provider abstraction layer with a real endpoint swap

### 1.2 Out of Scope

- LoRA model training (separate R&D stream)
- GCP Vertex AI evaluation (Phase 2 if Bedrock proves limiting)
- Character consistency pipeline (depends on LoRA stream)
- Style transfer via img2img (follows this migration)

---

## 2. Current Architecture

### 2.1 Key tables

The pipeline is controlled by three tables in the Xano data model:

**`data_models`** — provider abstraction layer. Each record defines prompt settings, model configuration, and output schema for a given generation type. The `type` field covers: `character-image`, `story-page-image`, `story-cover-image`. Fields: `slug`, `name`, `type`, `version`, `is_default`, `status`, `model_settings` (JSON), `prompt_template`, `output_schema` (JSON).

**`image_jobs`** — the job queue. Each record has: `job_type` (enum: `character-image`, `page-image`, `cover-image`), `status` (enum: `queued`, `processing`, `complete`, `error_retry`, `error_terminal`), `attempt`, `max_attempts`, `locked_until`, `retry_at`. Linked to `instant_stories`, `instant_story_pages`, and `characters` as appropriate.

**`executor_runs`** — full audit log per execution attempt. Stores `api_request`, `api_response`, `executor_result`, `started_at`, `completed_at`, linked to the parent `image_jobs` record.

The `data_models_id` is assigned at the `instant_stories` record level, meaning new stories can be pointed at a new `data_models` record without affecting in-flight or existing stories.

### 2.2 Current `data_models` record — page image (`tomale_story_page_image_v_1_0`)

```json
{
  "id": 5,
  "slug": "tomale_story_page_image_v_1_0",
  "name": "Tomale Page Image V1.0",
  "type": "story-page-image",
  "version": "1.0",
  "is_default": true,
  "status": "active",
  "model_settings": {
    "provider": "openai",
    "text": {
      "url": "https://api.openai.com/v1/chat/completions",
      "model": "gpt-4o-mini",
      "temperature": 0.35,
      "presence_penalty": 0.1,
      "frequency_penalty": 0.2,
      "max_completion_tokens": 4000
    },
    "image": {
      "url": "https://api.openai.com/v1/images/generations",
      "model": "dall-e-3",
      "size": "1792x1024",
      "n": 1
    },
    "pricing": {
      "text": { "input_per_million": 0.15, "output_per_million": 0.6 },
      "image": { "per_image": 0.08 }
    }
  },
  "output_schema": { "..." }
}
```

### 2.3 Current pipeline flow

```
Story created (instant_stories record, data_models_id assigned)
    → image_jobs record created (status: queued)
    → Xano background task (runs every 2 min) picks up queued image_jobs
    → Worker reads data_models record for config
    → Stage 1: POST /v1/chat/completions (gpt-4o-mini) → structured JSON page plan
    → Stage 2: POST /v1/images/generations (dall-e-3) → image URL
    → executor_runs record written (request + response)
    → Image stored as public file in Xano, attached to instant_story_pages record
    → token_usage record written
```

> **Storage note:** Images are currently stored as public files in Xano, secured behind user-scoped API queries. Per the CTO implementation plan, these should move to private files (Xano) or preferably S3 — cheaper, larger storage capacity, and enables archiving. This is a separate task but worth scheduling alongside or shortly after this migration.

---

## 3. Target Architecture — AWS Bedrock

### 3.1 Why AWS Bedrock first

Bedrock hosts Stability AI's SDXL as a managed inference endpoint. It requires no GPU instance management, bills per-image rather than per-hour, and applies against existing AWS credits. It is the lowest-friction path to validating the `data_models` provider abstraction before considering self-hosted GPU workers.

### 3.2 New `data_models` record

The migration creates a new record in `data_models`. No schema changes required. New stories are pointed at the new record via `data_models_id` on `instant_stories` — existing stories are unaffected.

```json
{
  "slug": "tomale_story_page_image_v_2_0",
  "name": "Tomale Page Image V2.0",
  "type": "story-page-image",
  "version": "2.0",
  "is_default": false,
  "status": "draft",
  "model_settings": {
    "provider": "aws_bedrock",
    "text": {
      "url": "https://api.openai.com/v1/chat/completions",
      "model": "gpt-4o-mini",
      "temperature": 0.35,
      "presence_penalty": 0.1,
      "frequency_penalty": 0.2,
      "max_completion_tokens": 4000
    },
    "image": {
      "url": "https://bedrock-runtime.<region>.amazonaws.com/model/stability.stable-diffusion-xl-v1/invoke",
      "auth": { "type": "aws_sigv4", "region": "<region>" },
      "modelId": "stability.stable-diffusion-xl-v1",
      "contentType": "application/json",
      "accept": "application/json",
      "body": {
        "cfg_scale": 7,
        "steps": 30,
        "seed": "<randomised per job>",
        "width": 1344,
        "height": 768,
        "style_preset": "<optional>"
      }
    },
    "pricing": {
      "text": { "input_per_million": 0.15, "output_per_million": 0.6 },
      "image": { "per_image": 0.04 }
    }
  },
  "output_schema": {
    "artifacts[0].base64": "string",
    "artifacts[0].finishReason": "string"
  }
}
```

> **Resolution note:** SDXL 1.0 does not natively support 1792×1024. The closest supported 16:9 resolution is 1344×768. This is a quality and aspect ratio trade-off to evaluate during testing.

**Key difference from v1:** Bedrock returns base64-encoded image bytes, not a URL. The worker output handler requires a small addition to decode the base64 payload and write it to storage before attaching the result to the `instant_story_pages` record. This has been validated as working in Xano. It is the only worker-side code change required.

---

## 4. Implementation Plan

### Phase 1 — AWS Bedrock (Days 1–2)

| # | Task | Notes |
|---|---|---|
| 1 | Enable SDXL in AWS Bedrock console | Request model access; may take up to 24h |
| 2 | Create IAM role with Bedrock invoke permissions | Scope to `bedrock:InvokeModel` on SDXL ARN only |
| 3 | Add AWS credentials to Xano environment variables | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` |
| 4 | Create new `data_models` record (`tomale_story_page_image_v_2_0`) | Status: draft; `is_default: false` |
| 5 | Update worker output handler to decode base64 → storage write | Validated working in Xano |
| 6 | Create test stories pointed at the v2 `data_models` record | Set `instant_stories.data_models_id` to v2 record id |
| 7 | Validate output — see Section 4.1 | Run 5–10 test stories before switching default |
| 8 | If validated: set `is_default: true`, point new stories at v2 | Roll back by reverting `is_default` |
| 9 | Repeat for `cover-image` and `character-image` job types | Create equivalent v2 records for each |

### 4.1 Testing approach

Because `data_models_id` is set at the `instant_stories` level, test stories can target the v2 record without touching production traffic. Run a minimum of 5–10 test stories across different themes and character configurations.

**Metrics to capture per test run:**

| Metric | Source | Target |
|---|---|---|
| Image quality | Visual review of generated pages | Comparable to DALL-E 3 output |
| Aspect ratio fidelity | Check stored image dimensions | 1344×768 rendered correctly |
| Generation speed | `executor_runs.started_at` → `completed_at` | Within 2–3 min per story |
| Cost per image | Bedrock billing console | ≤ $0.04–0.08 (confirm tier at 1344×768) |
| Error rate | `image_jobs.status`, `executor_runs` failures | 0 terminal errors on test batch |
| `token_usage` accuracy | Check `provider`, `model`, cost fields | Matches Bedrock invoice |

### Phase 2 — Self-hosted GPU workers on EC2 (if Bedrock proves limiting)

Bedrock does not natively support custom LoRA loading. When the LoRA character consistency pipeline is ready, self-hosted ComfyUI workers on EC2 GPU instances will be required. This phase uses the same `data_models` abstraction — ComfyUI exposes a REST API that maps cleanly to the existing record pattern.

The worker-tick architecture and `executor_runs` audit trail carry forward unchanged.

---

## 5. Pipeline Architecture

### 5.1 Phase 1 — AWS Bedrock flow

```
Story created (instant_stories.data_models_id → v2 record)
    → image_jobs record created (status: queued)
    → Xano background task (runs every 2 min) picks up queued image_jobs
    → Worker reads data_models record (slug: tomale_story_page_image_v_2_0)
    → Stage 1: POST /v1/chat/completions (gpt-4o-mini) → structured JSON page plan
    → Stage 2: Signs request using AWS SigV4
              → POST bedrock-runtime.../stability.stable-diffusion-xl-v1/invoke
    → executor_runs record written
    → base64 response decoded → image written to storage
    → instant_story_pages.image updated
    → image_jobs status → complete
    → token_usage record written (provider: aws_bedrock)
```

### 5.2 Phase 2 — Self-hosted ComfyUI flow (LoRA-ready)

```
image_jobs queue
    → Worker reads data_models record (e.g. character-image-lora-v1)
    → POST to ComfyUI REST API on EC2 GPU instance
    → LoRA model loaded per character
    → executor_runs record written
    → image written to storage
    → image_jobs status → complete
```

> At 1,000 users / weekly story cadence, 5 workers handles peak load within the 2–3 minute generation target. Workers scale with queue depth.

### 5.3 Img2img style pipeline — scoping note

Once self-hosted workers are live, an img2img approach becomes viable for both `page-image` and `cover-image` job types. The proposed two-stage flow:

1. **Stage 1 — content image:** Generate a raw scene image from character descriptions and the structured page plan (text-to-image, no style applied). This anchors character appearance and scene composition.
2. **Stage 2 — style pass:** Run img2img using the selected `artwork_style` (`image_prompt_positive` / `image_prompt_negative`) to apply the chosen visual style consistently across all pages of a story.

Advantages: style is applied uniformly in post; character consistency is easier to achieve in Stage 1 without fighting style prompts; artwork styles can be swapped without regenerating content images. Main cost is two inference passes per image. Full scoping and cost modelling should happen once Phase 2 workers are live — not a Phase 1 concern.

A further Phase 2 sub-slice, preserving the latent between passes, is specified in [[latent-preserving-regeneration-2026-05]].

---

## 6. Cost Model

### 6.1 Current cost — OpenAI DALL-E 3

The current `data_models` record uses `dall-e-3` at `1792x1024`, Standard quality. Cost per image: **$0.08**.

| Story length | Images (pages + cover) | Cost per story |
|---|---|---|
| 12 pages | 13 | $1.04 |
| 16 pages *(possible future)* | 17 | $1.36 |
| 20 pages *(possible future)* | 21 | $1.68 |

> 12-page stories (13 images) are confirmed V1. 16 and 20-page variants are included for planning purposes but not committed.

### 6.2 Target cost — AWS Bedrock SDXL

Bedrock SDXL 1.0 on-demand pricing:

| Resolution | Steps | Cost per image |
|---|---|---|
| 512×512 | ≤50 | $0.036 |
| 1024×1024 | ≤50 | $0.04 |
| 1024×1024 | >50 (premium) | $0.08 |

> SDXL 1.0 does not support 1792×1024. The nearest 16:9 equivalent is 1344×768. Confirm the cost tier for this resolution against the [Bedrock pricing page](https://aws.amazon.com/bedrock/pricing/) — expected to fall in the standard tier (~$0.036–$0.04).

Assuming ~$0.04/image:

| Story length | Images | Cost per story (Bedrock) | vs DALL-E 3 Standard | Saving |
|---|---|---|---|---|
| 12 pages | 13 | **$0.52** | $1.04 | ~$0.52 (50%) |
| 16 pages | 17 | **$0.68** | $1.36 | ~$0.68 (50%) |
| 20 pages | 21 | **$0.84** | $1.68 | ~$0.84 (50%) |

All costs apply against existing AWS credits (~£45k). Exact Bedrock cost at 1344×768 to be confirmed before committing.

### 6.3 Phase 2 — EC2 self-hosted spot pricing

> ```
> EC2 GPU instance estimates (spot pricing, April 2026):
>
> g4dn.xlarge  (T4,  16GB VRAM)  ~$0.16/hr spot  (~$0.46/hr on-demand)
> g5.xlarge    (A10G, 24GB VRAM)  ~$0.34/hr spot  (~$1.01/hr on-demand)
> p3.2xlarge   (V100, 16GB VRAM)  ~$0.92/hr spot  (~$3.06/hr on-demand)
>
> Spot = 60–70% reduction vs on-demand.
> Acceptable for image generation — image_jobs retry architecture
> already handles spot interruptions.
> NOT recommended for LoRA training jobs (use on-demand or reserved).
>
> At ~30s/image on g4dn.xlarge: ~120 images/hr ≈ $0.001/image compute cost.
> ```

### 6.4 LoRA character training cost (future)

At a $4.99 retail price per character, margin is approximately 75–77%. The first character can be offered free as an acquisition mechanic at a CAC of ~$1.15.

---

## 7. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Bedrock model access request takes >24h | Medium | Delays Phase 1 start | Submit access request before starting other tasks |
| SDXL 1344×768 quality noticeably inferior to DALL-E 3 HD 1792×1024 | Medium | Visual regression | Run visual comparison on 10+ stories before switching `is_default`; keep v1 record live for rollback |
| AWS SigV4 signing not natively supported in Xano | Medium | Blocks Bedrock auth | Validate signing approach in a spike before building out the full record; keep OpenAI fallback ready |
| `token_usage` cost tracking not aligned to Bedrock response shape | Low | Cost visibility gap | Update `provider` to `aws_bedrock`; cost is per-image not per-token — update `pricing.image.per_image` in v2 record |

---

## 8. References

### AWS Bedrock
- [Bedrock SDXL API docs](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-stability-diffusion.html)
- [Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)
- [IAM permissions for Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html)
- [AWS SigV4 signing](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html)
- [SDXL supported resolutions](https://stability.ai/sdxl-aws-documentation)

### ComfyUI (Phase 2)
- [ComfyUI repository](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI API documentation](https://github.com/comfyanonymous/ComfyUI/wiki/API)
- [Kohya-ss LoRA training](https://github.com/kohya-ss/sd-scripts)

### Cost benchmarks
- [SaladCloud SDXL benchmark (60k images, RTX 3090/4090)](https://blog.salad.com/stable-diffusion-xl-sdxl-benchmark/)
- [H100 rental price comparison (Nov 2025)](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison)
- [A100 on RunPod](https://www.runpod.io/gpu-models/a100-pcie)

### LoRA training
- [SDXL LoRA training guide 2025](https://sanj.dev/post/lora-training-2025-ultimate-guide)
- [LoRA training time estimates](https://www.propelrc.com/how-to-train-stable-diffusion-lora-models/)
- [IP-Adapter FaceID](https://github.com/tencent-ailab/IP-Adapter)

### Style transfer
- [LCM-LoRA for fast inference](https://huggingface.co/docs/diffusers/using-diffusers/inference_with_lcm_lora)
- [Regional prompting (ComfyUI)](https://github.com/huchenlei/ComfyUI-layerdiffuse)
