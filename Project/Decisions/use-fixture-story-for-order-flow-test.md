---
type: decision
title: use-fixture-story-for-order-flow-test
date: 2026-10-09
status: current
project: tomale-rn-v1
---

---

# Decision: Use a Pre-Completed Fixture Story for the Ordering Flow Test

## What we decided

The ordering flow (3A onward) runs against a pre-completed fixture story instead of waiting for generation on every run. Story generation gets its own poll-based test run in the Collection Runner or Newman (e.g. nightly), not in the monitor.

## Why

Run 1 failed at `3A-1` with `422 STORY_NOT_READY` because 3A fired straight after story creation and text plus image generation takes about 12–15 minutes. That confirmed the backend guard works, and that the ordering test cannot sit behind generation. A 12–15 minute generation also will not fit a monitor's run-time limit.

## Alternatives considered

- **Test-only generation stub flag** (like `pdf_force_success`) — noted as an option but not taken.

## Trade-offs accepted

The fixture story must belong to the test user, and the backend must allow re-ordering the same story; both are still to be confirmed.

## Workflow detail

3A was switched to the fixture story for run 2 (17:15 UTC). Generation is tested separately from ordering.

## Related notes

- [[simulate-stripe-payment-with-signed-postman-webhook]]
- [[replace-manual-test-gates-with-bounded-polling]]
- [[order-fulfilment-flow]]
- [[2026-10-09-001]]
