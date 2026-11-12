---
type: decision
title: "start-character-picture-on-create"
project: tomale-rn-v1
status: accepted
date: "2026-11-11"
related:
  - "[[2026-11-11-001]]"
  - "[[characters-create-hardening-brief]]"
  - "[[PRD-Characters]]"
affects:
  - "[[PRD-Characters]]"
  - "POST /characters"
  - "GET /characters"
  - "GET /characters/{characters_id}"
features:
  - F-characters
---

# Decision: start-character-picture-on-create

## What we decided

`POST /characters` starts the character's picture itself (option A), so one call creates the character and its picture. Character payloads expose a derived `picture_status` (`drawing` / `ready` / `failed`; failed after 15 minutes with no job). There is no `draft` character status, and no rename in V1.

## Why

The create endpoint did not start the picture: the app had to make a second call, so a picture could be missed. Found while writing the 008 micro-PRD alongside the other `POST /characters` gaps.

## Alternatives considered

Option B (keep the separate picture call from the app). A `draft` character status.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Recorded in [[characters-create-hardening-brief]] (the Xano brief for `POST /characters`, with moderation, story-ownership check, explicit inputs and trimmed response). 008 uses `picture_status`; the OpenAPI overlay (RS-2026-11-12-01) carries it in the generated character types.

## Related notes

[[2026-11-11-001]], [[characters-create-hardening-brief]], [[PRD-Characters]], [[add-character-story-count-and-story-filter]]
