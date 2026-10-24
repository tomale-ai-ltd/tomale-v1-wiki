---
type: decision
title: "per-child-story-visibility"
date: 2026-06-22
status: current
project: tomale-rn-v1
---

---

# Decision: per-child-story-visibility

## What we decided

A story on `instant_stories` is visible only to the profile that created it and any parent profile on the same account. There is no cross-profile or cross-account sharing in V1. Ownership is captured via a single FK `user_profiles_id` on `instant_stories`, set server-side at POST from `$auth.extras.active_profile.id` — never a client input. Read enforcement lives in the endpoint (GET all and GET one), not the frontend. Legacy stories with a null creator are backfilled to their account's default adult profile (`is_child == false`), so child profiles never inherit legacy content.

## Why

Keeps sibling content private by default without requiring a join table or sharing model in V1. Server-side assignment eliminates any client ability to spoof story ownership. Backfilling to the adult default is the safest ownership assumption for pre-profile content.

## Alternatives considered

A join table for story sharing (as specified in [[2-build-plan]]) was deferred — the full sharing model is out of scope for V1. No cross-profile visibility model was considered.

## Trade-offs accepted

No cross-profile or cross-account sharing in V1 is a deliberate scope reduction from the planned sharing model in the build plan. Users on the same account cannot share stories between sibling profiles. This is accepted to keep Phase 1 scope tight; the join-table model remains the intended V2 path.

## Workflow detail

On POST `instant_stories`, `user_profiles_id` is populated from `$auth.extras.active_profile.id` — the field is server-controlled and excluded from the client allow-list. GET all applies a nested profile and moderation gate in the `where` clause: parent profiles see all household stories; child profiles see only their own stories that have cleared moderation. GET one applies the same gate inside the existing precondition so a disallowed story returns 404 (covers another account, a sibling profile, a locked story, and a soft-deleted story — all indistinguishable to the caller). `bulk_assign_user_profiles_to_stories` migration ran to close the legacy data gap.

## Related notes

- [[2-build-plan]] — original sharing model that this deviates from
- [[5-cto-implementation-plan]] — Phase 1 checklist
- [[6-api-security-model]]
- [[fail-closed-active-profile-resolution]]
- [[parental-gate-on-profile-switch]]
