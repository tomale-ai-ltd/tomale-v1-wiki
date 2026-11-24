---
type: decision
title: "use-gemini-3-1-flash-image-on-vertex-eu-for-story-images"
project: tomale-rn-v1
status: proposed
date: "2026-11-24"
related:
  - "[[2026-11-24-002]]"
  - "[[image-pipeline-research-2026-11]]"
affects:
  - "[[PRD-Image-Pipeline]]"
  - "[[stack]]"
  - "data models (gateway records)"
features:
  - F-story-generation
  - F-characters
---

# Decision: use-gemini-3-1-flash-image-on-vertex-eu-for-story-images

## What we decided

**Proposed, subject to gates G0 and G1:**
- The primary image model is Gemini 3.1 Flash Image on the Vertex `eu` endpoint.
- Each character's portrait is passed as a labelled reference ("Reference image 1 = MIA …"), with at most 4 characters per image, plus the art style's sample image as a style-only reference.
- The prompt compiler moves to Gemini 3.1 Flash-Lite on `eu`.
- Nano Banana 2.1 (global only, about half the price) runs as the challenger in the bake-off.

## Why

It's the only credit-funded managed model with multi-reference character consistency and an EU endpoint, and it's GA with retirement no earlier than 28/05/2027. Imagen, Nova Canvas, Titan and SDXL are gone or deprecated. Google for Startups credits don't cover third-party Model Garden models.

## Alternatives considered

Nano Banana 2.1 and Gemini 3 Pro Image (global only); OpenAI gpt-image-2.6 (cash); self-hosted Qwen-Image-Edit or FLUX ([[defer-self-hosted-image-models-until-after-launch]]); Stability on Bedrock (us-west-2 only).

## Trade-offs accepted

- About £1.49 of credit per story at 2K, more than today, but paid from credits that would otherwise go unused.
- Child-filter risk (G0).
- Dynamic quota with no fixed RPM.
- A model move is due in Q2 2027.

## Workflow detail

Accept after [[IP-07-model-bake-off]] passes G1. If Nano Banana 2.1 wins and the DPIA accepts global processing, record that instead.

## Related notes

- [[IP-02-child-image-policy-spike]]
- [[measure-character-consistency-with-a-vlm-judge-and-blind-ratings]]
