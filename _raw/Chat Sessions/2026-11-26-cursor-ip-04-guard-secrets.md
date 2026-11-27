---
date: 2026-11-26
source: cursor
branch: chore/foundation
feature: IP-04 PR A guard secret reads
---

# Deny cloud secret/credential reads in guard

## What changed
- `18fb995` on PR #1: deny aws secret/credential get-* ops and gcloud auth token print / secrets versions access; tests for each.

## Decisions
- Kyle: secret-returning reads stay denied even when they match the read-shaped allow rule.

## Open questions / blockers
- None.

## Next
- Confirm `test` green.
