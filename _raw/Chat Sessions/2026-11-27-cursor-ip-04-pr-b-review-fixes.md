---
date: 2026-11-27
source: cursor
branch: 001-image-gateway
feature: IP-04 PR B review fixes
---

# Apply PR B contract review must/should fixes

## What changed
- `1519182` on PR #2: must-fix 1–6 and should-fix 7–10 from [[pr-b-contract-review]]; D1(a) and D2(a).
- Feasibility doc filled from review table; Q2 = `util.get_raw_input` with raw encoding.
- Analyze re-run (`specs/001-image-gateway/analyze-report.md`).

## Decisions
- Kyle D1(a) regenerate-then-fail; D2(a) signed URLs from cut-over.

## Open questions / blockers
- Session A items remain (dispatched, reaper, storage keys, unique index) — documented, not this PR.

## Next
- Confirm `test` green; Claude re-check; Kyle approves.
