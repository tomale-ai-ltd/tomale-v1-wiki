---
type: decision
title: "rename-user-profiles-is-default-to-is-primary"
date: 2026-06-30
status: current
project: tomale-rn-v1
---

---

# Decision: rename-user-profiles-is-default-to-is-primary

## What we decided

Rename the `user_profiles.is_default` column to `is_primary`, updated across the schema, all endpoints, and the `select_profile` function.

## Why

"Default" was an overloaded term. "Primary" reads more clearly and extends naturally to future multi-adult account support, where more than one adult profile could exist but only one is primary.

## Alternatives considered

Keeping `is_default` was the implicit alternative — rejected in favor of the clearer, more extensible name.

## Trade-offs accepted

None stated beyond the one-time migration cost of updating every reference. That cost was explicitly judged cheapest done now: "Renames are cheapest at first divergence — `is_default` → `is_primary` cost one endpoint today vs. six-plus in three months."

## Workflow detail

Schema column renamed; all endpoints referencing `is_default` updated; a residual `is_default` reference left over in `select_profile` was found and cleaned up in the same session.

## Related notes

- [[Sessions/2026-06-30-001]]
- [[prevent-deleting-active-profile-via-soft-delete]]
