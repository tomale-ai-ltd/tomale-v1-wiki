---
date: 2026-11-19
source: cursor
branch: 010-approvals
feature: 010-approvals
---

# Specified 010 approvals

## What changed
- Created branch `010-approvals` from main with `.specify/scripts/bash/create-new-feature.sh`. Nothing committed.
- Wrote `specs/010-approvals/spec.md` and `specs/010-approvals/checklists/requirements.md` from `.docs/prd/010-approvals.md` and the board copy in the vault `Project/Design/010-approvals/`.
- Uncommitted files carried off main onto this branch, still uncommitted: `api/client.ts` (Kyle's openapi update), `specs/009-profiles-pin/tasks.md` (T034 ticked), `.docs/prd/010-approvals.md`.

## Decisions
- Kyle asked to run `/speckit.specify` for slice 010 and to carry the uncommitted files onto the 010 branch rather than commit them to main.
- Signed-out approvals link follows oversight §8a: sign in, land on the primary parent, then the inbox. Picker and PIN are for a child session.
- Reject confirmation uses the board sentence, not the shorter line in the micro-PRD screen flow.
- Both story tiles show "Coming soon". Character tiles open the existing new-character form.
- RS-2026-11-18-02 was not applied. Help wording in the 009 spec was left as it is.

## Open questions / blockers
- Design boards are not copied yet. Kyle has not been asked to commit.

## Next
- On Kyle's go: copy `Project/Design/010-approvals/` into `specs/010-approvals/design/`, then commit `api/client.ts`, `.docs/prd/010-approvals.md`, the design folder, and the spec on `010-approvals`. Do not push. Leave the T034 tick out of that commit unless Kyle includes it.
