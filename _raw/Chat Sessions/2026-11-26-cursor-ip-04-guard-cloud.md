---
date: 2026-11-26
source: cursor
branch: chore/foundation
feature: IP-04 PR A guard cloud rules
---

# Position-aware fail-closed cloud guard

## What changed
- `fix(guard): position-aware read-only cloud rules` (`186d96b`) on PR #1.
- aws/gsutil/bq/gcloud classifiers no longer treat a read verb anywhere in argv as allow; unknown/unparseable cloud commands deny.
- Loophole deny cases + normal read allow cases in `tests/guard/`.
- PR description answers: contracts path, checkov/tflint → IP-08, cloud read-only vs mutate/unknown.

## Decisions
- Kyle: Cloud Run group `run` is not mutating when a later positional is a read verb (`run services describe`).

## Open questions / blockers
- None for this fix.

## Next
- Confirm `test` green; Kyle merges when ready.
