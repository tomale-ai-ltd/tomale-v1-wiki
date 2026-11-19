---
date: 2026-11-19
source: cursor
branch: 010-approvals
feature: 010-approvals
---

# Planned 010 approvals

## What changed
- Wrote `specs/010-approvals/plan.md`, `research.md`, `data-model.md`, `copy.md`, `quickstart.md`, and `contracts/approvals.openapi.yaml`.
- Updated `.cursor/rules/specify-rules.mdc` from the plan. Not committed.

## Decisions
- `approvalsStore` is memory only, with a Principle 4 exception. It does not use `StoriesStore`. The count is `awaiting.length`.
- Pictures are mapped per surface. Home and inbox use `cover_image`. The child waiting card draws no cover. Nulls get a placeholder.
- Names match `profilesStore` on `user_profiles_id` with no coercion. The list field is an integer and profile ids are UUIDs, so a failed match reads "A story".
- Keep is assign, then approve. A failed approve leaves Approve and Delete story, toasting "Approved. It's in your stories."
- `tomalerntest` and `tomale` are already the schemes. No EAS rebuild.
- The phone list is for Kyle. The plan does not start Metro or the simulator.

## Open questions / blockers
- Whether the live list `user_profiles_id` will ever equal a profile UUID. The plan does not coerce it.

## Next
- Kyle reviews the plan, then `/speckit.tasks`. Do not push.
