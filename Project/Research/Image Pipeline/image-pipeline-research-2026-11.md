---
type: research
title: image-pipeline-research-2026-11
project: tomale-rn-v1
status: current
date: 2026-11-24
owner: vault
related:
  - "[[PRD-Image-Pipeline]]"
  - "[[image-pipeline-plan]]"
  - "[[image-pipeline-future-state]]"
  - "[[bedrock-image-migration-plan-2026-04]]"
  - "[[latent-preserving-regeneration-2026-05]]"
features:
  - F-story-generation
  - F-characters
---

# Image pipeline research: OpenAI → credit-funded GCP + AWS (24/11/2026)

Research run in the Claude Project chat on 24/11 (Advanced Research), after an interview with Kyle. Sources were official GCP, AWS and OpenAI docs first, then model providers, then third parties. This note keeps the findings, evidence, vendor evaluation and cost model. Scope and requirements are in [[PRD-Image-Pipeline]], diagrams in [[image-pipeline-future-state]], and tasks in [[image-pipeline-plan]].

**Replaces** [[bedrock-image-migration-plan-2026-04]] as the working input. SDXL and Nova Canvas on Bedrock are no longer an option (below).

## Corrections and checks made after the report (24/11)

- **Checked on OpenAI's deprecations page:**
  - `gpt-image-1.5` shuts down on 1 Dec 2026; the replacement is `gpt-image-2.6-sunburst` or `-flare`.
  - `gpt-image-2` shuts down on 10 Feb 2027.
  - `gpt-4o-mini` shuts down on **14 Jan 2027** (replacement `gpt-6-luna`).
  - `gpt-4o-mini-tts` and `tts-1` shut down on **6 Jan 2027** (replacement `gpt-realtime-2.1-mini`).
  The report treated gpt-4o-mini as a long-term rollback; it isn't one.
- **From the Xano mirror:**
  - Page and cover executors load the default record by type at run time, not the story's `data_models_id`. So a record can't be trialled on test stories just by pointing a story at it, as the April plan assumed.
  - Character images use the record pinned on each character.
- **Credits corrected 26/11 (Kyle): $10k AWS and $25k GCP**, in dollars; the report assumed £10k and £25k (≈$12.7k and ≈$31.7k). The burn-down below still fits: about $10.8k of $25k GCP and under $0.4k of $10k AWS by 30/06/2027.
- **Kyle's answers (24/11):** AWS credits are £10k (the vault figure, since corrected), from AWS Activate and Google for Startups, nothing spent yet; live before launch; keep the Papermill title overlay; defer upscaling until a printed proof; all tier 0 and 1 art styles; in house unless a partner is fully credit-funded.

## Key findings

1. **Today's model is ending.** `gpt-image-1.5` stops on 1 Dec 2026 → [[image-pipeline-session-0-brief]].
2. **Several options in the brief no longer exist:**
   - Imagen 3/4 on Vertex were shut down 30 Jun 2026 (replacement named: `gemini-nano-banana-2.1`).
   - Gemini 2.5 Flash Image was shut down 2 Oct 2026.
   - Amazon Nova Canvas reached end of life 30 Sep 2026, and Titan Image v2 on 30 Jun 2026.
   - SDXL is deprecated.
   - Stability's current Bedrock models run in us-west-2 only.
3. **Google's Nano Banana family is the only credit-funded managed option with multi-reference character consistency.**
   - **Gemini 3.1 Flash Image** (`gemini-3.1-flash-image`): GA 28 May 2026, retirement "May 28, 2027 or later". Regions `global`, `us` and `eu`. Up to 14 references, editing and multi-turn editing.
   - **Nano Banana 2.1:** GA 6 Oct 2026, about half the price, but its Vertex page lists the `global` endpoint only.
   - Reported limits: 4 character references (Pro: 5) and 10 object references.
4. **Credits:**
   - Google for Startups covers Google's own products (Gemini, Vertex, Cloud Run, GPUs) but **not third-party models in Model Garden or Marketplace**. FLUX or Qwen offered as partner models would be paid in cash.
   - AWS Activate covers eligible AWS services and, by exception, third-party models on Bedrock. It excludes other Marketplace purchases, Professional Services and upfront RI/Savings Plans.
   - Neither pays for an implementation partner. Ask the Google Startup Success Manager and the AWS Activate contact anyway.
5. **Child images are the critical risk.**
   - Vertex `personGeneration` has `ALLOW_ALL` (adults and children), `ALLOW_ADULT` and `ALLOW_NONE`.
   - The Gemini image Responsible AI page lists a "Child" filter (codes 58061214 / 17301594) that blocks child content not allowed by the request settings "or allowlisting". A separate filter (64151117) catches photorealistic children. No allowlisting procedure is published.
   - Forum reports (anecdotal) say Veo blocked stylised 3D children while Gemini image did not.
   - → Day-1 spike, gate G0 ([[IP-02-child-image-policy-spike]]).
6. **Throughput is limited by Xano, not the model** (5-minute tick, serial pool).
   - Gemini image models run on dynamic shared quota with no fixed RPM ("Fixed quota: Not supported").
   - Forum reports describe 429s at about 7 concurrent requests on `global`.
   - So the design must rate-limit (Cloud Tasks) rather than fan out freely.
7. **Embedding metrics alone don't measure stylised identity.**
   - In Adobe's "Beyond the Pixels" (arXiv:2511.08087) on cartoon characters, human–human agreement was 0.83. A VLM judge correlated 0.50 with humans, DINOv2 0.34 and CLIP 0.20.
   - EntityBench (May 2026) found DINOv2 measures generic similarity, not identity.
   - → VLM-as-judge per attribute is the main automated metric, DINOv2 a drift alarm, and blind human rating the release gate.

## Evidence table (late 2026)

| Item | Fact |
|---|---|
| gpt-image-1.5 | Shutdown 1 Dec 2026 → gpt-image-2.6-sunburst / -flare (OpenAI deprecations page) |
| gpt-image-2.6 | Released 4 Nov 2026; generations and edits only; $30 per 1M image output tokens; `complexity` low/medium/high, default high; base64 output |
| Gemini 3.1 Flash Image | GA; `global` / `us` / `eu`; up to 14 refs; 1,120 tokens per input image; output $0.045 (512), $0.067 (1K), $0.101 (2K), $0.15 (4K) |
| Nano Banana 2.1 | GA 6 Oct 2026; `global` only; ≈$0.0336 (1K), $0.0504 (2K), $0.113 (4K) |
| Gemini 3 Pro Image | $0.134 (1K/2K), $0.24 (4K); `global` only |
| Gemini 3.1 Flash-Lite (text) | $0.25 / $1.50 per 1M in/out (global), slightly more on `eu`; `global`, `us`, `eu` |
| Cloud Run GPU | L4 24 GB or RTX PRO 6000 96 GB; L4 in europe-west1/4 (not London); scales to zero; an always-on L4 ≈ $764/month |
| FLUX licences | Kontext [dev], FLUX.2 [dev], [klein] 9B non-commercial (paid licence); [klein] 4B Apache-2.0 |
| Qwen-Image-Edit-2511 | Apache-2.0, 20B BF16, multi-image input (best with 1–3) |
| Rekognition moderation | $0.0010 per image, first 1M (US East example; check eu-west-2) |
| Vertex quotas | Dynamic shared quota; the global endpoint "doesn't support data residency requirements" |

To re-check in the consoles: the Nano Banana 2.1 reference limits, the `eu` price premium (assumed ≤10%), and the eu-west-2 Rekognition price.

## Vendor evaluation (scores 1–5, weighted)

**Image model:**

| Option | Score | Note |
|---|---|---|
| **Gemini 3.1 Flash Image, `eu`** | **4.25** | Primary: EU processing, credits, multi-reference, retires after credit expiry |
| Nano Banana 2.1, `global` | 4.15 | Challenger in the bake-off; half the cost if the DPIA accepts global processing |
| Gemini 3 Pro Image, `global` | 4.05 | Quality option for covers |
| Qwen-Image-Edit-2511 self-hosted | 3.65 | Best open option (Apache-2.0); heavy GPU, slow cold start; post-launch |
| FLUX.1 Kontext / FLUX.2 [dev] self-hosted | 3.5 | Needs a paid BFL licence |
| FLUX.2 [klein] 4B self-hosted | 3.4 | Apache-2.0, weaker on consistency |
| OpenAI gpt-image-2.6 | 3.35 | Fallback record: proven, paid in cash |
| Stability on Bedrock | 3.15 | us-west-2 only |
| SDXL + IP-Adapter (ComfyUI) | 3.05 | Most build effort |

**Other tasks:**

| Task | Primary | Fallback |
|---|---|---|
| Prompt compiler | Gemini 3.1 Flash-Lite on `eu` (≈$0.02 per book) | Gemini Flash; `gpt-6-luna` (gpt-4o-mini ends 14/01) |
| Queue and workers | Xano → Cloud Run gateway → Cloud Tasks → Cloud Run worker → Xano webhook | Pub/Sub push; SQS + Lambda |
| Storage | S3 eu-west-2 private + CloudFront OAC + Lambda signer (1-hour URLs) | GCS + Cloud CDN signed URLs |
| Output moderation | Provider filters + Rekognition + Gemini VLM judge, mapped to `moderation-image` | Cloud Vision SafeSearch |
| Evaluation | Python harness: character crops, DINOv2/CLIP drift alarm, VLM attribute and bleed judge, Character-F1, blind human rating | Vertex Gen AI evaluation service |
| IaC and observability | Terraform (google + aws), checkov/tflint, GitHub Actions with WIF to both clouds; Cloud Monitoring, CloudWatch, budgets at 25/50/75% | — |

**Calling the model directly from Xano was rejected:** it keeps the serial bottleneck. The executor pattern stays, but executors *dispatch* to the gateway, and results come back through a webhook, like the HPBC callbacks.

## How the model knows who is who

1. **Labelled references.** Each portrait is its own image part, preceded by a text part such as "Reference image 1 = MIA (girl, 6, curly red hair, yellow raincoat)". SUBJECT and COMPOSITION name characters by that label. This is the default; validate binding on the golden set.
2. **Character sheet.** A front, three-quarter and back turnaround made once from the approved portrait, used as that character's single reference slot.
3. **Style reference.** `artwork_style.sample_image`, labelled "style only, don't copy characters".
4. **At most 4 referenced characters per image.** The compiler demotes extras to background figures.
5. **A repair pass, not chained pages.** Feeding in the previous page forces pages to run one after another and raises bleed. Use edit or mask passes only to fix one failing character on a flagged page.
6. Regional prompting, masks and composite grids are SDXL/ComfyUI techniques, so Option B only. Published evidence on bleed is thin; Tomale measures its own bleed rate.

## Cost model

**Base case** (Flash Image `eu`, 2K, 3 refs, 15% regeneration allowance):
- ≈ $0.131 per delivered image.
- **≈ $1.89 (≈ £1.49) GCP per story** including one portrait, plus ≈ $0.03 AWS.
- Today: ≈ £1.20 total AI per story, with ≈ $0.78 of that being images.

**Other options:**
- Nano Banana 2.1 at 2K: ≈ $0.86 of images per story.
- Flash Image at 1K: ≈ $1.14.

**Burn-down to 30/06/2027** (100 stories in Feb → 500 in Mar → 2,000 in Jun):
- ≈ $10.8k of the $25k GCP credit is spent (corrected 26/11; the report assumed ≈ $31.7k).
- Under $0.4k of the $10k AWS credit is spent.
- **Under-use is the issue, not runway.**
  - Spend headroom only where the evals show it pays: Pro for covers, two candidates per page with the judge picking.
  - Move other OpenAI cash spend (text, TTS) onto credits.

**After the credits:** about £1.52 per story on the base case; £0.70–0.90 on Nano Banana 2.1 or 1K plus upscaling. Plan a cost bake-off for May 2027.

Assumption: £1 ≈ $1.27.

## Risks (summary; detail in [[PRD-Image-Pipeline]])

- OpenAI shutdowns: 1 Dec, 6 Jan and 14 Jan.
- The child filter blocking chibi child characters.
- 429s on dynamic quota.
- Flash Image retiring from May 2027.
- Nano Banana 2.1 being global-only.
- Credit expiry.
- Xano limits on signing and async.
- The holidays shortening the calendar.

## Sources (main)

- OpenAI deprecations: https://developers.openai.com/api/docs/deprecations
- OpenAI Image API reference: https://developers.openai.com/api/reference/resources/images/methods/generate
- Gemini 3.1 Flash Image: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-1-flash-image
- Nano Banana 2.1: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/nano-banana-2-1
- Gemini image Responsible AI: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/gemini-image-responsible-ai
- PersonGeneration: https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/rest/Shared.Types/PersonGeneration
- Model versions: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions
- Locations: https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/locations
- Standard PayGo / dynamic shared quota: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/standard-paygo
- Vertex pricing: https://cloud.google.com/vertex-ai/generative-ai/pricing
- Cloud Run GPU: https://docs.cloud.google.com/run/docs/configuring/services/gpu
- Google for Startups: https://cloud.google.com/startup
- BFL licensing: https://help.bfl.ai/articles/9272590838-self-serve-dev-license-overview-pricing
- Beyond the Pixels: arXiv:2511.08087 · StoryWeaver: arXiv:2412.07375
- Forum reports (anecdotal): 429s on Flash Image (discuss.ai.google.dev/t/178939); child-filter false positives on Veo (discuss.ai.google.dev/t/131917)
