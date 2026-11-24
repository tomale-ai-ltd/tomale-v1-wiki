---
type: decision
title: "defer-self-hosted-image-models-until-after-launch"
project: tomale-rn-v1
status: proposed
date: "2026-11-24"
related:
  - "[[2026-11-24-002]]"
affects:
  - "[[roadmap]]"
  - "[[v2-backlog]]"
features:
  - F-story-generation
---

# Decision: defer-self-hosted-image-models-until-after-launch

## What we decided

Self-hosted open-weight models (Option B) aren't built before launch. They stay a post-launch third provider, used if child-filter blocks or price make them worth it.
- First candidate: Qwen-Image-Edit-2511 (Apache-2.0) on Cloud Run GPU or GKE.
- FLUX Kontext / FLUX.2 [dev] need a paid commercial licence.

## Why

Kyle's rule (24/11): test both if there's time, otherwise lean to managed APIs if self-hosting is complex.
- **Size:** the strongest commercially licensed editor is 20B parameters and needs a 96 GB GPU, or quantisation to fit an L4.
- **Cold start:** loading tens of GB of weights dominates it.
- **Effort:** more build and maintenance than a solo founder can absorb before January.

## Alternatives considered

Building both now (doesn't fit the calendar); SDXL + IP-Adapter in ComfyUI (most effort, weaker quality).

## Trade-offs accepted

Dependence on Google's child-content filtering until a third provider exists. This is mitigated by the OpenAI fallback.

## Workflow detail

Revisit after launch, or earlier if G0 fails. Add to [[v2-backlog]].

## Related notes

- [[use-gemini-3-1-flash-image-on-vertex-eu-for-story-images]]
- [[image-pipeline-research-2026-11]]
