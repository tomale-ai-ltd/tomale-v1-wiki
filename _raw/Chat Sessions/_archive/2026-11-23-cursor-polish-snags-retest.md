---
date: 2026-11-23
source: cursor
branch: polish-snags
feature: polish-snags, RS-2026-11-18-02
---

# Follow-up snags S-023 to S-030

## What changed
- `be6e901` S-023, `9cdd91b` S-024, `05f3003` S-025, `576b50b` S-026, `9d85c4c` S-027, `6e9b267` S-028, `391264f` S-029, `3781a06` S-030.
- PR #33 into main: https://github.com/tomale-ai-ltd/tomale-rn-test/pull/33. Not merged. GitHub `test` check passed.
- `pnpm check` and `pnpm test` passed (18 suites, 121 tests).

## Decisions
- Kyle's snag pass: Settings uses the compact ScreenHeader. Change PIN is a secondary button. "PIN changed" uses the same confirmation toast as "Coming soon". Forgot PIN has no envelope. The book mark stays above the picker list when offline.
- Cursor: the stretched back control was the page-band button, not the shared compact header. Every Manage profiles picture keeps a transparent ring so the active one does not shift.

## Open questions / blockers
- Kyle still to retest S-023 to S-030 on the phone. Snag status in the vault was not updated.

## Next
- Kyle retests, then merges PR #33 if the pass is clean.
