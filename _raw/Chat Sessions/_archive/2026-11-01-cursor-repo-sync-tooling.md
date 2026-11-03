---
date: 2026-11-01
source: cursor
branch: repo-sync/2026-11-01-tooling
feature: RS-2026-10-30-03, RS-2026-10-30-05, RS-2026-11-01-02, RS-2026-11-01-05
---

# Repo-sync tooling PR A opened

## What changed
- Opened PR #15: https://github.com/tomale-ai-ltd/tomale-rn-test/pull/15.
- Branch commits:
  - `c7a01ae` RS-2026-10-30-03 Move tooling to Node 22 LTS
  - `3dad170` RS-2026-10-30-05 Add Renovate dependency reviews
  - `e916aae` RS-2026-11-01-02 Add CI security scans
  - `ac0e715` RS-2026-11-01-05 Document repo-sync rule
- The required GitHub `test` check passed on the PR.

## Decisions
- Kyle approved stopping at an open PR; Kyle merges, and Claude records the main-branch hashes after merge.
- Cursor used Semgrep 1.182.1 because 1.183.0 was less than 7 days old.
- Gitleaks 8.30.1 allowlists AWS keys ending in `EXAMPLE`; the local canary used the Gitleaks v8.30.1 AWS sample format so the default rule failed as expected.
- The `pnpm audit` gate needed a `follow-redirects` override and one-off `minimumReleaseAgeExclude`; the patched version was 6 days old. New Expo CLI `node-forge` advisories were added to the existing accepted audit-ignore list.

## Open questions / blockers
- None for PR A. Kyle still needs to install the Renovate GitHub App on `tomale-ai-ltd/tomale-rn-test` after merge.

## Next
- Kyle reviews and merges PR #15 by rebase. Claude records the main hashes against the repo-sync items after merge.
