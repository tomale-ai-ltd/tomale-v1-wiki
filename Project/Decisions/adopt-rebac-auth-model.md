---
type: decision
title: adopt-rebac-auth-model
date: 2025-01-01
status: current
project: tomale-rn-v1
---

---

# Decision: Adopt ReBAC Authorization Model

## What we decided

Use Relationship-Based Access Control (ReBAC) as the authorization model for
all user-owned data, implemented as an owner-or-deny-all default in Xano.

All queries enforcing user data access use:
```sql
WHERE owner_user_id = auth.user.id
```

## Why

The CTO review demonstrated that without ownership-based authorization, any
authenticated (or unauthenticated) user could access or delete other users'
data by guessing integer IDs. A simple ownership filter closes this
immediately.

ReBAC was chosen over the alternatives because:
- RBAC (Role-Based): better suited to organizational hierarchies with defined
  roles — overkill for a consumer app where the primary distinction is
  "your data vs not your data"
- ABAC (Attribute-Based): most powerful but highest engineering complexity —
  inappropriate for a solo V1 build

ReBAC offers the right balance: relationship-aware access (owner, child profile
assignment) without the complexity of a full attribute-based system.

## Alternatives considered

- **RBAC** — rejected: role explosion risk, doesn't naturally model
  parent/child data relationships
- **ABAC** — rejected: high DIY effort, unnecessary complexity for V1
- **No formal model** — rejected: demonstrated vulnerability in CTO review,
  PII exposed publicly

## Trade-offs accepted

- Slightly more verbose queries (every user-data query includes ownership filter)
- Child profile access requires an additional validation layer per request

## Consequences

- All Xano tables with user-owned data must have `owner_user_id` field
- All queries against user-owned data must include ownership filter
- Child profile access uses a two-layer check: parent owns the data AND
  child profile is assigned to that content
- Future extensibility (public library, cross-user sharing) deferred to post-V1

## Related notes

- [[3-cto-tech-review]]
- [[5-cto-implementation-plan]]
- [[Repos/tomale-rn-test/memory/data-model|data-model]]
- [[6. Backend - Xano]]
