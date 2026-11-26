---
type: plan-task
id: IP-02
title: "G0: child-image policy spike"
status: done
owner: "Claude (script), Kyle (runs)"
depends:
  - "[[IP-01-credits-and-accounts]]"
gate: "G0"
effort_days: 1
target: 2026-11-28
scoping: test-plan
project: tomale-rn-v1
---

# IP-02: G0: child-image policy spike

**Goal:** Generate 50 chibi pages with child characters (tier 0/1 styles) with `personGeneration: ALLOW_ALL` on Flash Image `eu` and global, and Nano Banana 2.1 global; log finish reasons and filter codes.

**Done when:** G0: under 2% child-filter blocks on `eu`. Otherwise: request allowlisting, keep OpenAI as default for launch, and raise the self-hosted option.

**Notes:** Test plan only: prompts, counts, pass rule. Results table in the session note. This gate can change everything after it, so nothing past IP-04 is specified in detail before it passes.

Plan: [[image-pipeline-plan]] · Scope: [[PRD-Image-Pipeline]]

## Log
- **26/11:** GCP project `tomale-image-dev` (Vertex API on, budget £400 with Savings excluded, ADC login, no keys). Script `~/Developer/tomale/spikes/g0/g0_spike.py` (google-genai 3.6.1, `person_generation=ALLOW_ALL`, 1K).
- **26/11 smoke test (`--limit 3`, 13 calls per target):** 39/39 OK, **0 child blocks** on eu-flash, global-flash and global-nb21.
  - Latency p50: 9.2 s eu-flash, 9.1 s global-flash, 16.0 s Nano Banana 2.1.
  - Claude's visual check: the portraits match their descriptions; the two-character labelled-reference pages keep each child's hair and clothes, with no bleed; style changes correctly.
  - One nit: Ollie's shirt has a "7" on it, picked up from the portrait (counts as stray text).
  - Next: the full run, 165 calls.
- **26/11 full run (55 calls per target, 165 in total): G0 PASSED.**
  - 165/165 OK: 0 child blocks, 0 other blocks, 0 errors, 0 rate-limit retries (3 parallel workers).
  - Latency p50/p95: eu-flash 8.9/11.2 s, global-flash 8.9/12.4 s, Nano Banana 2.1 17.0/23.1 s.
- **Claude's visual check (eu-flash) found no bleed.** All 5 two-character pages kept each child's hair, clothes and features. Findings for G1 and prompt tuning:
  1. **Style drift with references:** two-character pages asked for soft 3D chibi came out in a painted 2D picture-book style. The style prompt alone doesn't hold when references are passed, so test the `artwork_style.sample_image` as a style reference in IP-07.
  2. **Stray numbers:** football shirts got numbers ("7", then "8"). Add "no numbers on clothing" to the constraints, or describe shirts as plain.
  3. **Outfits applied literally:** Mia wears her raincoat and wellies in bed. Whether the JSON outfit is fixed or adapts to the scene is a product question for the compiler prompt.
