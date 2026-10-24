---
type: decision
title: "avoid-column-named-function-inputs-in-xano"
date: 2026-10-15
status: current
project: tomale-rn-v1
---

---

# Decision: avoid-column-named-function-inputs-in-xano

## What we decided

Never name a Xano function input or variable after a column the function writes to. Where a clash exists, fix it by renaming the input (e.g. `created_at` to `run_created_at`, `message` to `update_message`).

## Why

Xano's hidden-fields behaviour writes any function input/variable named like a column into that column. This overwrote `store_orders.created_at` with the executor run timestamp (via `papermill_generate_pdf_cover` / `_inner`) and the buyer's gift message with Pureprint text on every HPBC callback (via `hpbc_update_order`).

## Alternatives considered

Enabling `enforce_hidden_fields` was rejected: unlisted fields may reset to the table default.

## Trade-offs accepted

Not discussed in session notes. A Xano AI sweep for other inputs/variables named like columns was requested; results are pending.

## Workflow detail

Review function inputs and variables against the columns they write when building or editing Xano functions. Both HPBC status callback endpoints now map `message` to `update_message`, and `pdf_worker_tick` passes `$now` as `run_created_at`.

## Related notes

- [[2026-10-14-001]]
- [[2026-10-15-001]]
- [[add-temporary-audit-trigger-on-store-orders]]
- [[enforce-forward-only-hpbc-callback-status-transitions]]
- [[restrict-store-orders-message-to-buyer-gift-message]]
- [[find-executor-runs-by-id-not-timestamp]]
