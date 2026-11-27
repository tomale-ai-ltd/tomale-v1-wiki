---
type: brief
title: ip-06-cursor-brief
project: tomale-rn-v1
status: draft
date: 2026-11-27
related:
  - "[[IP-06-eval-harness]]"
  - "[[IP-07-model-bake-off]]"
  - "[[measure-character-consistency-with-a-vlm-judge-and-blind-ratings]]"
  - "[[Project/Plan/image-pipeline/golden-set/README|golden set v1]]"
---

# IP-06: evaluation harness (Cursor brief)

Speckit feature **002-eval-harness** in `tomale-image-gateway`. A command-line harness that runs the golden set through **pipelines** (today's OpenAI baseline and the Gemini candidates), scores the output with a **VLM judge**, and produces a **blind rating page** for Kyle and parents. It feeds the bake-off (IP-07, gate G1).

## Kyle's acceptance checks (what "done" looks like)

1. `eval plan --pipeline baseline` prints the job list and an estimated cost (156 OpenAI images, about $8–16) **without calling anything**.
2. `eval run --pipeline baseline` produces 156 images (12 stories × 12 pages + cover) and a manifest. **Running it again costs nothing**, because outputs are cached.
3. `eval run --pipeline gemini-flash-eu` produces the same 156 images on Vertex `eu`, using the 24 portraits generated once on Gemini and passed as labelled references.
4. `eval judge` writes a report per pipeline covering:
   - attribute accuracy per character (hair, eyes, clothing, age, species, from the JSON)
   - bleed rate
   - extra-character rate
   - stray text or number rate
   - style match and plot match
   - blocks, latency and cost
   On G01 (Postman Pip) it should catch the lost blue postman outfit on the baseline.
5. `eval rate` opens a local web page showing the two pipelines' versions of each page side by side, **without saying which is which**, and saves 1–5 ratings (consistency, style, plot) to a CSV. Kyle and 2–3 parents can use it.
6. `--max-usd` stops a run before it overspends. OpenAI calls need an explicit `--allow-openai` flag.
7. No key in the repo: Google uses your gcloud login (ADC); the OpenAI key comes only from `OPENAI_API_KEY` in your shell.

## Design constraints

- **The baseline must reproduce today's pipeline exactly.** Port the page and cover image prompt templates **verbatim** from the Xano mirror:
  - `Repos/tomale-xano/function/ai_pipeline_executor_page_image.xs` (the page template: STYLE `artwork_style.description`, SUBJECT, BACKGROUND, COMPOSITION, MOOD `theme.image_keywords`, CONSTRAINTS)
  - `ai_pipeline_executor_cover_image.xs` (lines ~276–284: STYLE, the raw planner JSON, MOOD, CONSTRAINTS)
  - the planner prompts and schemas from the `data_models` records
  Planner: `gpt-4o-mini`, with temperature and penalties as in the records. Image: `gpt-image-2.6-flare`, `1536x1024`, no `quality` parameter (as Xano sends). Freeze the record snapshots by copying `tomale-v1-wiki/Project/Plan/image-pipeline/golden-set/data_models-baseline-2026-11-24.json` to `eval/golden/v1/data_models.json`.
- **Candidate pipelines are configuration, not code:** a YAML file per pipeline (planner model, image model, endpoint, size, reference strategy, style reference on or off) with adapters behind it, the same adapter interface IP-09 will use. Initial candidates:
  - `gemini-flash-eu`: Flash Image `eu`, labelled portraits plus the style sample image as a style-only reference, 2K
  - `gemini-flash-eu-1k`
  - `nb21-global`: Nano Banana 2.1 global
  - `gemini-flash-eu-norefs`: text only, to measure what the references add
- **Labelled references:** each portrait is an image part preceded by "Reference image N = NAME (short description)". At most 4 per image; the planner names characters by label.
- **Portraits:** generated once on Gemini from each character's JSON (24 in all), cached, and shared by the judge and every candidate. Existing Xano pictures are never used.
- **Judge:** a Gemini vision model on `eu` (default `gemini-3.1-flash-lite`; check the model id on its model page), with JSON-schema output. Per page:
  - for each character the plan includes: present? every JSON attribute matches? which reference does this figure match (bleed)?
  - extra characters, stray text or numbers, guideline breaches (scary content, copyright)
  - style match, plot match to the page text
  Validate the judge on 20 pages that Kyle spot-checks.
- **Drift metrics** (DINOv2/CLIP on character crops): optional, behind `--drift`. Not needed for G1.
- **Golden set:** copy `golden-set-v1.json` into `eval/golden/v1/` and verify its sha256 (`3fc315d9…68bd8`, in the vault README). Generated images go in `eval/output/`, which is gitignored and never committed.
- **Agents never run paid commands.** Cursor may run `eval plan`, `--dry-run` and unit tests only; **real runs are started by Kyle**. Put this in `.cursor/rules/tomale-gateway.mdc`.
- **Tests:** unit tests with mocked providers for every pipeline, the cache, the cost ceiling, judge parsing and the rating export. CI green.

## Process

Kyle runs each step himself, stopping where marked:
1. Micro-PRD `.docs/prd/002-eval-harness-micro-prd.md` from this brief.
2. `/speckit.specify` → `/speckit.clarify`. Paste the clarify questions to Claude; Kyle answers the product ones.
3. `/speckit.plan` → `/speckit.analyze` → **stop, open a PR, and let Claude review** the spec and plan.
4. After review: `/speckit.tasks` → `/speckit.implement` on the same branch. PR green. Kyle runs acceptance checks 1–7.

## Prompt for Cursor (step 1–3)

> Work only in `~/Developer/tomale/tomale-image-gateway`: `cd` there, pull `main` and create branch `002-eval-harness`. Read `tomale-v1-wiki/Project/Plan/image-pipeline/ip-06-cursor-brief.md` and write `.docs/prd/002-eval-harness-micro-prd.md` from it, keeping Kyle's seven acceptance checks word for word as acceptance criteria. Then stop and tell me it's ready for `/speckit.specify`.
