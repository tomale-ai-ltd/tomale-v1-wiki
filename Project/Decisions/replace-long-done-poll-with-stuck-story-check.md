---
type: decision
title: replace-long-done-poll-with-stuck-story-check
project: tomale-rn-v1
status: accepted
date: 2026-10-12
features:
  - X-testing
---

# Decision: replace-long-done-poll-with-stuck-story-check

## What we decided

A stuck-story check (`1C`) replaces the long poll waiting for a story to reach Done in monitor-sized runs. It fails if any story has sat in a non-terminal state longer than `stuckStoryMaxAgeMin` (default 45 minutes).

## Why

The Postman monitor can't run the Stripe CLI or wait 12–15 minutes, so a long Done poll doesn't fit a monitor run. The stuck-story check detects the failure mode actually seen (stories stranded at In Queue) without waiting.

## Alternatives considered

Keeping the long Done poll was the existing approach; it was dropped for monitor runs because of the time limit. Not otherwise discussed.

## Trade-offs accepted

1C detects stranded stories rather than proving a fresh story completes end to end; that still needs a manual or Runner check. 1C will also fail until the four currently stuck stories are recovered or marked Blocked.

## Workflow detail

The `_tests` collection starts with 1C, then the story flow, then orders. The full unattended Runner run is still outstanding, and monitor setup (run-time limit, secret-type `stripe_webhook_secret`) is still to be decided.

## Related notes

- [[Sessions/2026-10-12-001]]
- [[replace-manual-test-gates-with-bounded-polling]]
- [[simulate-stripe-payment-with-signed-postman-webhook]]
- [[story-creation-flow]]
- [[formalise-story-status-lifecycle]]
- [[verify-stripe-checkout-totals-against-xano-prices]]
