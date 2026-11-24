---
type: decision
title: measure-character-consistency-with-a-vlm-judge-and-blind-ratings
project: tomale-rn-v1
status: accepted
date: 2026-11-24
related:
  - "[[2026-11-24-002]]"
affects:
  - "[[PRD-Image-Pipeline]]"
  - "[[test-suite]]"
features:
  - F-story-generation
  - X-testing
---

# Decision: measure-character-consistency-with-a-vlm-judge-and-blind-ratings

## What we decided

Consistency and bleed are measured on a frozen golden set of 10 existing stories (pages, portraits, JSON characters, styles):
- **Primary automated metric:** a VLM judge answering per-attribute questions from the JSON character model, plus "which reference is this?" for bleed. It also gives Character-F1 and Frame-Accuracy.
- **Drift alarm, not a gate:** DINOv2/CLIP similarity of character crops to the portrait.
- **Release gate:** blind human rating (1–5 for consistency, style and plot match) by Kyle and 2–3 parents.

The baseline is today's OpenAI output.

## Why

On cartoon characters, research shows VLM judges track human judgement far better than CLIP or DINOv2 (Adobe, arXiv:2511.08087; EntityBench 2026).

## Alternatives considered

Embedding scores only; human rating only (too slow to iterate on).

## Trade-offs accepted

The judge costs credits and is itself imperfect, so humans gate the release.

## Workflow detail

The harness lives in the gateway repo and runs in CI on prompt or model changes ([[IP-06-eval-harness]]).

## Related notes

- [[IP-05-golden-set]]
- [[IP-07-model-bake-off]]
