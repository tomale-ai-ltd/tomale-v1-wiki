---
type: decision
title: prevent-deleting-active-profile-via-soft-delete
project: tomale-rn-v1
status: accepted
date: 2026-06-30
---

---

# Decision: prevent-deleting-active-profile-via-soft-delete

## What we decided

`DELETE /user_profiles/{id}` (soft-delete) blocks deleting the profile that is currently active in the requesting session — the profile referenced by `active_profile.id` in the JWT. Enforced via a precondition that fails with `422 CANNOT_DELETE_ACTIVE`.

## Why

Without this guard, a parent could soft-delete the profile their own token is currently pointing at, leaving the JWT's `active_profile.id` referencing a row that no longer resolves — a broken-token state for the rest of that session.

## Alternatives considered

Not discussed in session notes — the guard was built directly alongside the existing guard against deleting the primary/default profile, with no alternative approach recorded.

## Trade-offs accepted

A parent must switch to a different profile before they can delete the one currently in use. This adds a step to the delete flow but avoids the broken-token state described above.

## Workflow detail

Implemented as a precondition inside the soft-delete endpoint (`deleted_at = now`, parent-only), alongside the existing guard against deleting the primary profile. Covered by the endpoint's test suite (8/8 green, including the cap-count interaction case).

## Related notes

- [[Sessions/2026-06-30-001]]
- [[fail-closed-active-profile-resolution]]
- [[6-api-security-model]]
