---
type: research
title: latent-preserving-regeneration-2026-05
project: tomale-rn-v1
status: historical
date: 2026-05-08
owner: vault
related:
  - "[[roadmap]]"
  - "[[bedrock-image-migration-plan-2026-04]]"
features:
  - F-story-generation
---

> **Imported 28/10/2026** from the Claude chat "AI image generation through model delegation" (08/05/2026). It was drafted as a Phase 2 sub-slice of [[bedrock-image-migration-plan-2026-04]] and is kept as input for the image-pipeline research track ([[roadmap]] §6). **It is not current.**
> - The "#1 gotcha" it names (character consistency) now applies to `gpt-image-1.5`.
> - The `max_regenerations = 1` rule comes from the PoD PRD, which is being reworked around entitlements ([[gate-image-generation-with-entitlements-at-story-creation]]).
> - The latent sizes and the "under 50%" target are unmeasured estimates.
>
> The CfI "Boosting Fathers' Engagement" application (`Project/Research/Research Proposals/`) has the later SDXL + LoRA + IP-Adapter design this builds towards.

# Phase 2 — Sub-slice: Latent-Preserving Regeneration

## Concept

Decouple "what is in the image" from "how the image looks" by preserving the SDXL latent representation between generation and decode. This enables style and appearance changes without regenerating the underlying composition.

In a standard pipeline, a single SDXL pass produces a latent and immediately decodes it to pixels via the VAE. The latent is discarded. This sub-slice persists the latent as a first-class artefact, allowing multiple decode passes against the same composition.

## Background techniques

From the originating discussion: an image's information can be produced without rendering pixels, because decoding is the last, separable step of a diffusion pipeline.

1. **Latent passing.** Model A produces a latent; model B applies a LoRA and decodes it. ComfyUI workflows do this routinely.
2. **ControlNet / IP-Adapter conditioning.** Model A produces structural or semantic guidance (depth, pose, edges, an image embedding) that constrains model B.
3. **Prompt or embedding handoff.** Model A produces an embedding tuned for model B's latent space.

Managed endpoints (Bedrock SDXL) don't expose intermediate latents, so this needs self-hosted inference (ComfyUI).

## Why this matters for Tomale

1. **Cheaper regenerations.** When a parent dislikes the visual style (not the content) of a generated page, re-running only the style application pass avoids re-paying for the full diffusion process. Directly relevant to the `max_regenerations = 1` rule in the Order & PoD PRD — gives users more meaningful retries within the cap.
2. **Style swap as a product feature.** Users could preview the same story in multiple art styles (watercolour, line art, pastel) without regenerating the scene. Opens a potential premium tier feature.
3. **Character consistency (paired with IP-Adapter FaceID).** Holding the composition latent constant while applying character conditioning via IP-Adapter gives tighter cross-page consistency than prompt-only approaches — the #1 known gotcha with the current DALL-E 3 pipeline.
4. **Batch efficiency.** Content latents for all 13 pages of a story can be generated in one batch; style application runs as a separate, cheaper batch. Reduces total inference time per story.

## Pipeline

**Pass 1 — Content latent generation**
- Input: prompt derived from page text + character JSON + scene context
- Model: SDXL base (no LoRA, no style conditioning)
- Output: latent tensor, persisted to S3 as `.safetensors`
- Stored on: new `image_latents` table, FK to `instant_story_pages.id`

**Pass 2 — Style application**
- Input: latent from Pass 1 + style LoRA + IP-Adapter character ref
- Model: SDXL with Tomale style LoRA applied
- Output: final image, written to existing `instant_story_pages.image`

## Data model additions

`image_latents` table:
- `id`
- `instant_story_page_id` (FK, nullable for cover images)
- `instant_story_id` (FK, for cover images)
- `latent_url` (S3, private bucket)
- `seed`
- `prompt_hash`
- `model_version`
- `created_at`

Existing `image_jobs` table extended:
- `job_type` enum gains: `content-latent`, `style-apply`
- `parent_latent_id` (nullable FK to `image_latents`)

## Trade-offs

- **Doubled inference time per image** vs single-pass. Acceptable given jobs are already user-perceived async via the worker tick pattern.
- **Storage cost.** Latents are ~5–10MB each; a 13-page story adds ~100MB to S3. Negligible at current scale, worth modelling at 10k stories/month.
- **Pipeline complexity.** ComfyUI workflow gains a checkpoint/resume pattern. Worth it only if style-swap or regeneration savings are productised — not just technically possible.
- **Phase dependency.** Requires self-hosted ComfyUI (Phase 2 work). Not achievable on managed Bedrock SDXL, which doesn't expose intermediate latents.

## Open questions

- Is "regenerate with same composition, different style" a feature Tomale wants to ship, or just a cost-saving mechanism behind the existing regeneration UX?
- Should latents be retained indefinitely, or expired after the order is sent to print?
- Does style-swap need its own entitlement / pricing model, or is it rolled into the existing regeneration cap?

## Acceptance criteria

- A page image can be regenerated with a new style LoRA in under 50% of the time/cost of a full single-pass regeneration (target to replace with a measured baseline).
- The same content latent produces visibly distinct outputs under different style LoRAs while preserving composition.
- `image_latents` records survive page regeneration cycles and can be reused.
- No latent data is exposed via public S3 URLs.
