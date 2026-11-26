---
type: plan-task
id: IP-02
title: "G0: child-image policy spike"
status: in-progress
owner: "Claude Code (script), Kyle (runs)"
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
