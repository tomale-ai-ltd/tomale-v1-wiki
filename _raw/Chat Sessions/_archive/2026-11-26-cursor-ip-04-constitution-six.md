---
date: 2026-11-26
source: cursor
branch: chore/foundation
feature: IP-04 PR A constitution 1.0.0
---

# Apply approved six-principle gateway constitution

## What changed
- Replaced `.specify/memory/constitution.md` with vault `gateway-constitution-draft.md` (below the HR) verbatim; kept version 1.0.0 footer; Sync Impact Report: initial adoption, six principles, replaces unmerged nine-principle draft.
- `plan-template.md` Constitution Check now lists Principles 1–6 gates from the Development Workflow section (only Spec Kit delta vs rn-test `@05f27b1`).
- Aligned `.cursor/rules/tomale-gateway.mdc` and README to the six principles.
- Commit `7bcf6eb` on PR https://github.com/tomale-ai-ltd/tomale-image-gateway/pull/1.

## Decisions
- Kyle approved the six-principle draft; Cursor applied it without rewording.

## Open questions / blockers
- Listed on the PR: Spec Kit feature-local `specs/.../contracts/` vs repo-root `contracts/gateway.openapi.yaml`; checkov/tflint deferred to IP-08; guard “cloud changes” vs read-only describe/list/get.

## Next
- Wait for `test` green; Kyle merges PR #1 when ready. PR B not started.
