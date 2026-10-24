---
type: decision
title: "defer-documentation-refresh-until-after-phase-1-signoff"
date: 2026-10-14
status: current
project: tomale-rn-v1
---

---

# Decision: defer-documentation-refresh-until-after-phase-1-signoff

## What we decided

The batch documentation refresh happens after Phase 1 sign-off and before Cursor frontend work. Scope: `api-spec`, `data-model`, `6-api-security-model`, the PRDs (Mixam to Pureprint), the Postman OpenAPI re-sync, and the Claude project knowledge copies.

## Why

The batch update was agreed on 2026-05-15 for the end of Phase 1, and reconfirmed on 30 Jun, 16 Jul and 8 Oct (with a specific drift list).

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Docs stay out of date until sign-off.

## Workflow detail

Sign-off steps: update `6-api-security-model`, decide the fate of `/admin/upload/image`, then start the refresh.

## Related notes

- [[adopt-openapi-import-for-postman-collection-sync]]
- [[place-frontend-development-on-hold]]
- [[2026-10-14-001]]
