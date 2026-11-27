---
type: prd
title: PRD-Image-Pipeline
project: tomale-rn-v1
status: draft
version: 0.1
date: 2026-11-24
last_verified: 2026-11-24
owner: vault
features:
  - F-story-generation
  - F-characters
  - X-security
  - X-platform
related:
  - "[[image-pipeline-research-2026-11]]"
  - "[[image-pipeline-future-state]]"
  - "[[image-pipeline-plan]]"
  - "[[image-generation-flow]]"
  - "[[migrate-image-storage-to-aws-s3-signed-urls]]"
---

# PRD: Image pipeline on GCP + AWS credits

> **Draft 0.1 (24/11/2026).** From Kyle's brief and interview (24/11) and [[image-pipeline-research-2026-11]]. Kyle approves → `current`. Decisions are proposed in `Project/Decisions/` (listed in §9).

## 1. Overview

Story covers, pages and (if the gate passes) character pictures move from OpenAI's image API to a credit-funded pipeline:
- **On Google Cloud:** a Cloud Run gateway behind the existing Xano `image_jobs` pipeline, with Gemini 3.1 Flash Image on Vertex `eu` as the model and labelled character references.
- **On AWS London:** private S3 with CloudFront signed URLs, and Rekognition for output moderation.
- **Kept on OpenAI:** an OpenAI record as the fallback provider.

It must be live **before the late-January 2027 launch** (Kyle, 24/11), built in parallel with the app work.

## 2. Goals

- **G1** Replace OpenAI image generation with a credit-funded pipeline before launch. OpenAI's own shutdowns force at least one model change on 1 Dec ([[image-pipeline-session-0-brief]]).
- **G2** Characters stay consistent across a story, at least as well as on `gpt-image-1.5`, with no attribute bleed. Reference images are passed for pages and covers (today only character pictures use one).
- **G3** 95% of books finish within 3 minutes. Waking from idle adds at most 2 minutes.
- **G4** Every output image is moderated against the Tomale content guidelines.
- **G5** Images are private in AWS London and served by 1-hour signed URLs.
- **G6** `image_jobs` and the app contract stay unchanged; models can be swapped through `data_models.model_settings`.
- **G7** Both credit pools are used efficiently ($25k GCP, $10k AWS, both expiring 30/06/2027; corrected by Kyle 26/11 from £); no cost when idle.

## 3. Scope

**In:**
- Cover, page and character-picture generation (the character picture is gated, §6 G3).
- The prompt compiler.
- The gateway, queue and callback.
- S3, CloudFront and URL signing.
- Output moderation.
- The golden set and evaluation harness.
- Terraform, observability and runbooks.
- Replacing the other OpenAI models that shut down before launch (`gpt-4o-mini` 14/01, `gpt-4o-mini-tts` 6/01): [[IP-03-replace-text-and-voice-models]].

**Out:**
- LoRA training.
- A/B testing (offline shadow comparison only).
- Parent-uploaded photos as references.
- Changes to Papermill (it keeps the cover title overlay with per-template fonts), print partners or app UI.
- Upscaling, until a printed proof shows it's needed.
- Self-hosted open models before launch.

## 4. Requirements

| # | Requirement | Type | How it's met | Verified by |
|---|---|---|---|---|
| R1 | Integrate with orchestrator → tick → executor | Must | Executors get a `provider: tomale_gateway` branch that posts the job and sets `dispatched`; results return through an HMAC-signed Xano webhook; the tick keeps its kill switch, reaper and leases | Postman contract folder; shadow run |
| R2 | All 13 images, a whole book queued at once | Must | The orchestrator dispatches the whole book straight away; Cloud Tasks fans out within rate caps | Load test: 20 books at once |
| R3 | Consistency ≥ today, from the JSON character model | Must | Labelled portrait references, character sheet and JSON attributes in the prompt | Golden-set evals and blind ratings (§6) |
| R4 | Efficient use of both credits | Must | Generation, LLM and queue on GCP; storage, CDN, signer and Rekognition on AWS; budgets at 25/50/75%, tracking gross spend (credits/Savings excluded) ([[track-cloud-budgets-on-gross-spend]]) | Monthly burn-down |
| R5 | Sleep mode | Must | Cloud Run and Lambda scale to zero; the model API costs nothing idle | Billing after an idle week |
| R6 | Legible text in images | Must (low) | Evaluated for in-scene text; the title stays with Papermill | 20 sign/label prompts in the eval |
| R7 | Secure storage, access via Xano and the app | Must | Private S3, CloudFront OAC, signer Lambda; Cloud Run → AWS through OIDC federation, no stored AWS keys; no GCP service account keys: ADC for people, Workload Identity Federation for CI and services ([[use-no-service-account-keys-on-gcp]]) | Security review, IAM Access Analyzer |
| R8 | Highly available and resilient | Must | Cloud Tasks retries, task name = job id and attempt, terminal-failure callback, idempotent webhook, fallback record | Chaos tests |
| R9 | Style, page plot and characters captured | Must | Style sample image and style prompt; compiler output {subject, background, composition} | VLM judge |
| R10 | Content guidelines, including children | Must | `personGeneration`, provider filters, Rekognition, VLM guideline check, mapped to `moderation-image` enforcement | Red-team prompt set; G0 |
| R11 | All tier 0 and 1 art styles | Must | Style reference and prompt per `artwork_style` | Golden set covers every style |
| N1 | No inconsistent characters | Must not | R3 plus the repair pass on flagged pages | Bleed and consistency thresholds |
| N2 | No attribute bleed | Must not | One labelled reference per character, max 4 per image, bleed check in the judge | Bleed rate ≤ baseline |
| C1 | Reference images | Nice | Generated portraits only | Eval |
| C2 | Multi-character consistency across images | Nice | Same references for every page | Eval |
| C3 | Speed | Nice | G3 | Load test |
| C4 | Character pictures through the same pipeline | Nice | Gateway edit mode, after its own eval | G3 gate |
| C5 | Demand-based scaling | Nice | Cloud Run autoscaling under Cloud Tasks caps | Load test |
| C6 | Swappable models | Nice | Provider adapters keyed by `model_settings.provider` and `model` | Switch test |

## 5. Contract (unchanged for the app)

- `image_jobs` stays the interface. The only additions are status `dispatched`, and a storage key on the target record next to the native image field.
- The app reads image URLs as today; Xano fills them from the signer.
- `data_models` records select the provider. One default per type; an OpenAI record stays as the fallback.

## 6. Gates (acceptance)

- **G0 child-image policy:** under 2% child-filter blocks over 50 chibi child pages on `eu`, else escalate (allowlisting, fallback, Option B) ([[IP-02-child-image-policy-spike]]).
- **G1 quality:** the chosen model and settings score at least the baseline on blind human consistency, have a bleed rate no worse than baseline, and reach ≥ 90% VLM attribute accuracy on the golden set ([[IP-07-model-bake-off]]).
- **G2 live:** book p95 under 3 minutes at 20 concurrent books, no lost or duplicate jobs, chaos tests converge, no high security findings, printed proof approved, rollback drilled in under 5 minutes.
- **G3 character pictures:** the same eval on portraits before the character executor moves.

## 7. Assumptions

- Volume of 100 stories a month in February, 500 in March and 2,000 by June 2027, each with about one new character picture.
- 2K output is good enough for A4 print, pending a printed proof.
- EEA processing is covered for UK GDPR (confirm in the DPIA).
- Kyle has about half his time for this until launch.

## 8. Risks

| Risk | Mitigation |
|---|---|
| OpenAI shutdowns: images 1/12, TTS 6/01, gpt-4o-mini 14/01 | Session 0 this week; IP-03 in Session A |
| Child filter blocks chibi children; no published allowlist route | G0 on day 1; request allowlisting through the Startup Success Manager; OpenAI fallback; Option B post-launch |
| 429s on dynamic shared quota | Cloud Tasks rate caps and backoff; overflow to the fallback |
| Flash Image retires from 28/05/2027 | Provider adapters; plan the move to the successor in Q2 2027 |
| Nano Banana 2.1 is global-only | Stay on `eu` until the DPIA accepts global or an EU endpoint appears |
| Credit expiry 30/06/2027 | Cost per job tracked; May 2027 cost bake-off |
| Xano limits (signing, async) | Signing in Lambda; idempotent webhook; contract tests first |
| Holidays shorten the calendar | Bake-off and infrastructure done before 19/12; cut-over by 13/01 |

## 9. Decisions (proposed 24/11)

- [[repoint-image-models-to-gpt-image-2-6-before-shutdown]]
- [[generate-story-images-through-a-cloud-run-gateway-with-xano-callbacks]]
- [[use-gemini-3-1-flash-image-on-vertex-eu-for-story-images]] (waits for G1)
- [[keep-openai-image-record-as-fallback-provider]]
- [[sign-image-urls-with-a-lambda-signer-behind-cloudfront]]
- [[moderate-generated-images-in-three-layers]]
- [[measure-character-consistency-with-a-vlm-judge-and-blind-ratings]]
- [[build-image-infrastructure-in-a-cursor-terraform-repo]]
- [[defer-self-hosted-image-models-until-after-launch]]

## 10. Open questions

- Is a Vertex allowlisting route for child content needed? Depends on G0.
- Does the Startup Success Manager or AWS Activate contact have a credit-funded partner offer?
- `gpt-6-luna` vs Gemini for Xano's own text calls (moderation, story text, chat), and the TTS replacement: decided in IP-03.
- Do generated character pictures, processed in the EU, need any new wording in the DPIA or Privacy Notice?
