---
type: plan-task
id: IP-02
title: "G0: child-image policy spike"
status: todo
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
