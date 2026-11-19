---
date: 2026-11-19
source: cursor
branch: 010-approvals
feature: 010-approvals
---

# Committed the 010 spec and the B6 list types

## What changed
- `89b1e0e` Record the approvals spec, micro-PRD, and boards. Includes the specify checklist.
- `d23837e` B6: user_profiles_id on the story list; nullable pictures. Overlay, `xano.yaml` (codegen reads it), `api/client.ts`, the awaiting-list fixture, and the overlay test.
- `6c9a7ad` Mark the profiles and PIN phone pass done. T034 only.
- Not pushed. `pnpm typecheck` passed. `pnpm test` 97 passed. No caller needed a placeholder; nothing failed typecheck.

## Decisions
- Kyle asked for the three commits on `010-approvals`, and for the list field to be integer int64 nullable on the full story only.
- `&urlImage` is nullable, so the list cover, the story's character pictures, page images, and the artwork sample are `| null`.
- Spec text was left for Kyle to take into clarify.

## Open questions / blockers
- None from this step.

## Next
- Kyle runs `/speckit.clarify`. Do not push until he asks.
