---
type: decision
title: moderate-generated-images-in-three-layers
project: tomale-rn-v1
status: accepted
date: 2026-11-24
related:
  - "[[2026-11-24-002]]"
  - "[[moderate-free-text-instructions-with-moderation-text-policy]]"
affects:
  - "[[story-creation-flow]]"
  - "[[PRD-Image-Pipeline]]"
  - data models (moderation-image)
  - moderation_flags
features:
  - X-security
  - F-story-generation
---

# Decision: moderate-generated-images-in-three-layers

## What we decided

Every generated image is checked before it's stored or shown:
1. **Provider safety filters.** `personGeneration` is set explicitly. A safety finish is retried once with a softened prompt, then the job ends `error_terminal`.
2. **Amazon Rekognition** moderation labels.
3. **A Gemini Flash-Lite VLM judge** against the Tomale content guidelines: copyrighted characters, violence, scary content, stray text, extra characters. The same call runs the attribute and bleed checks.

The policy lives in a `moderation-image` data model record (the type already exists, unused). Results map to the existing enforcement values; `flag_account` writes `moderation_flags`.

## Why

No output image is moderated today. A children's product needs output checks as well as the existing input checks. Keeping the policy in `data_models` matches the text moderation pattern.

## Alternatives considered

Provider filters only (not Tomale's guidelines); Cloud Vision SafeSearch instead of Rekognition (kept as fallback).

## Trade-offs accepted

About $0.004 and a few seconds per image. Some false positives get regenerated.

## Workflow detail

A red-team prompt set is part of the eval harness. Thresholds are agreed in IP-04.

## Related notes

- [[PRD-Image-Pipeline]]
- [[image-pipeline-research-2026-11]]
