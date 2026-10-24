---
type: decision
title: formalise-story-status-lifecycle
project: tomale-rn-v1
status: accepted
date: 2026-10-12
---

---

# Decision: formalise-story-status-lifecycle

## What we decided

Story status lifecycle is formalised as Draft → Preparing → In Queue → Done, with Blocked set from moderation. `story_completion_check` now keys off `status == "In Queue"`, and the moderation pass branch keys off the schema's actual `enforcement` value (`"none"`).

## Why

Four test stories were stuck at In Queue. Two bugs caused it: moderation branched on `enforcement == "pass"` while the schema returns `"none"`, so status was never written; and `story_completion_check` required Preparing, but page text sets In Queue first.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Moderation fail-open was re-rated normal priority because the child-visibility allow-list (Pass, or Parental Approval + `parent_approved`) protects children; hardening (fail-closed `else`, consistent result shape) is deferred but still planned.

## Workflow detail

`Project/Architecture/story-creation-flow.md` was refreshed with the lifecycle and known gaps. The Postman 2B test now asserts synopsis, `In Queue` and `Pass`. The four stuck stories must be recovered or marked Blocked, and moderation branches checked against schema enum spelling.

## Related notes

- [[Sessions/2026-10-12-001]]
- [[story-creation-flow]]
- [[PRD-Chatbot-Story-Conversations]]
- [[6-api-security-model]]
- [[verify-stripe-checkout-totals-against-xano-prices]]
- [[replace-long-done-poll-with-stuck-story-check]]
