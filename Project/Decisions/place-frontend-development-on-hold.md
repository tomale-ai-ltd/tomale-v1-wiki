---
type: decision
title: place-frontend-development-on-hold
date: 2025-12-27
status: current
project: tomale-rn-v1
---

---

# Decision: place-frontend-development-on-hold

## What we decided

To pause the development of the crossplatform react native frontend for Tomale V1, and switch focus to a series of backend / tech stack improvements based on the CTO tech review.

## Why 

The CTO tech review identified several critical issues that, if left unresolved, would compound as the frontend grows: - All Xano API endpoints were publicly accessible without authentication — including destructive operations and PII-containing user records - No separation between dev and production environments — all testing was happening against live data - No ownership-based authorization model — any user could access or modify another user's data by guessing integer IDs - No secrets management — API keys potentially exposed in the repository - No meaningful test coverage or CI security checks Continuing frontend development on top of an insecure and unstructured backend would mean building features against an API that will change significantly once the security model is properly implemented. The cost of rework increases the further development progresses before these foundations are fixed. 
## Alternatives considered

**Continue frontend development in parallel** — rejected: 

- new frontend features would be built against endpoints that are about to be restructured, renamed, or deleted entirely per the API surface reduction work. High rework cost.

**Fix security issues without pausing frontend** — rejected: 

- the ownership model changes (adding `owner_user_id`, scoped queries, soft deletes) will break existing frontend API calls. 
- A clean pause avoids mid-feature breakage. 

## Trade-offs accepted 

- Delay to V1 feature completion while backend work is underway 
- Frontend momentum is lost and will need to be rebuilt when work resumes 
- Some backend changes may still require frontend adjustments on resumption

## Consequences

- All active Cursor frontend work paused at Slice 000 foundations
- Development focus switches to the 5-phase CTO implementation plan
- Frontend resumes once Phase 1 (Security & Data Integrity) and Phase 2 (Environments & Observability) are complete
- Resumption point: Slice 000 foundations are largely complete
- frontend work resumes at Slice 100 (Characters)

## Related notes 

- [[3-cto-tech-review|3-cto-tech-review]]
- [[4-cto-improvements-list|4-cto-improvements-list]]
- [[5-cto-implementation-plan|5-cto-implementation-plan]]
- [[12. CICD - EAS, GitHub|12. CICD - EAS, GitHub]]
- [[6. Backend - Xano|6. Backend - Xano]]
