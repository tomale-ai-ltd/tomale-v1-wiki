---
type: decision
title: keep-openai-image-record-as-fallback-provider
project: tomale-rn-v1
status: accepted
date: 2026-11-24
related:
  - "[[2026-11-24-002]]"
affects:
  - "[[PRD-Image-Pipeline]]"
  - "[[image-generation-flow]]"
  - data models
features:
  - F-story-generation
---

# Decision: keep-openai-image-record-as-fallback-provider

## What we decided

An OpenAI `gpt-image-2.6` record stays live for each image type after the cut-over.
- **Rollback:** make it the default again.
- **Overflow:** the gateway can also use it, through its OpenAI adapter, when Vertex is unavailable or repeatedly blocks a job.

## Why

It's the proven path, it needs no new Xano code, and it gives a rollback in minutes. It also covers child-filter blocks or quota exhaustion on Vertex.

## Alternatives considered

No fallback (rollback would mean a code change); a self-hosted fallback (not before launch).

## Trade-offs accepted

Fallback use is paid in cash. OpenAI model shutdowns must be watched, and the record kept on a current model.

## Workflow detail

The record is created in Session A. Rollback is drilled in IP-17.

## Related notes

- [[repoint-image-models-to-gpt-image-2-6-before-shutdown]]
- [[generate-story-images-through-a-cloud-run-gateway-with-xano-callbacks]]
