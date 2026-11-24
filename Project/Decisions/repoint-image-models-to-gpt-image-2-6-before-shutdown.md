---
type: decision
title: "repoint-image-models-to-gpt-image-2-6-before-shutdown"
project: tomale-rn-v1
status: proposed
date: "2026-11-24"
related:
  - "[[2026-11-24-002]]"
  - "[[image-pipeline-session-0-brief]]"
affects:
  - "[[image-generation-flow]]"
  - "[[stack]]"
  - "[[backend-xano]]"
  - "data models (story-page-image, story-cover-image, character-image)"
features:
  - F-story-generation
  - F-characters
---

# Decision: repoint-image-models-to-gpt-image-2-6-before-shutdown

## What we decided

Before 1 December 2026, the page, cover and every in-use character `data_models` record moves from `gpt-image-1.5` to `gpt-image-2.6-flare`. The records are edited in place: model name, `pricing.image.per_image` and `version`. Sunburst is used only if Flare is clearly worse in the smoke test.

## Why

OpenAI removes `gpt-image-1.5` from the API on 1 Dec 2026. `gpt-image-2` also leaves on 10 Feb 2027, so the 2.6 family is the only OpenAI choice that lasts to launch. The 2.6 models take the same request fields and return base64 like today, so no executor change is needed. Flare is the faster variant at the same price.

## Alternatives considered

- `gpt-image-2`: rejected, it shuts down 10 Feb 2027.
- New records with a default switch: rejected for Session 0, because character pictures are pinned per character and rollback to 1.5 is impossible after 1 Dec.
- Going straight to Vertex: not possible in a week.

## Trade-offs accepted

- Paid in cash until the new pipeline is live.
- The `complexity` field can't be set without a code change, and defaults to high (possibly slower).
- Record history lives in the session note, not git.

## Workflow detail

Steps, checks and rollback are in [[image-pipeline-session-0-brief]].

## Related notes

- [[image-pipeline-session-0-brief]]
- [[image-pipeline-research-2026-11]]
- [[keep-openai-image-record-as-fallback-provider]]
