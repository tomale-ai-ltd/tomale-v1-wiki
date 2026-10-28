---
type: decision
title: log-only-small-status-fields-in-executor-runs
project: tomale-rn-v1
status: accepted
date: 2026-10-21
features:
  - X-security
  - F-story-generation
  - F-print-fulfilment
---

# Decision: log-only-small-status-fields-in-executor-runs

## What we decided

`executor_runs` logs only small status fields (request `url`/`method` and response `status`), never full payloads. Applied to the Papermill PDF runs, which previously saved the entire API response into `executor_runs.api_response`.

## Why

The PDF response is 4–30 MB; saving it caused the final edit to fail silently, leaving PDF runs stuck in `queued`.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Same change set fixed `$api_status` being declared before the try, `"402"` to `402`, and the cover filename now using `$story.title`. Related to the executor run lookup by id change.

## Related notes

- [[find-executor-runs-by-id-not-timestamp]]
- [[image-generation-flow]]
- [[order-fulfilment-flow]]
- [[2026-10-21-001]]
