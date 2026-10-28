---
type: decision
title: split-list-and-detail-projections
project: tomale-rn-v1
status: accepted
date: 2026-06-22
features:
  - F-bookshelf
---

# Decision: split-list-and-detail-projections

## What we decided

GET all `instant_stories` returns a lightweight card projection. GET single returns a curated detailed projection. The two projections intentionally differ. The field difference is a UX and performance choice, not a security boundary — anything that must never reach a client is excluded from both projections.

## Why

List views need only enough data to render a card (title, thumbnail, status). Pulling heavy fields — long text, pages/reviews addons — on every list item wastes bandwidth and slows the client. The detail view can afford a fuller payload because it loads one record at a time.

## Alternatives considered

Using a single projection for both endpoints was not explicitly discussed and is implicitly rejected by the implementation.

## Trade-offs accepted

Two projections must be maintained in sync when the schema changes. Field additions need to be evaluated for each projection independently. This maintenance cost is accepted as preferable to over-fetching on list views.

## Workflow detail

GET all card projection excludes heavy pages/reviews addons and long text fields. GET single returns a curated superset of the card fields. After trimming the card projection, `xano.yaml` and the generated `client.ts` should be regenerated (noted as a follow-up). Security-sensitive fields are excluded from both projections at the data layer, not via frontend filtering.

## Related notes

- [[per-child-story-visibility]]
- [[6-api-security-model]]
