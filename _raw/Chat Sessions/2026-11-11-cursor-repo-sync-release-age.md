---
date: 2026-11-11
source: cursor
branch: repo-sync/2026-11-11
feature: RS-2026-11-05-06 and RS-2026-11-04-01
---

# Remove the temporary release-age excludes and the @swc/helpers override

## What changed
- PR #25, not merged. `7713046` RS-2026-11-05-06 drops the 007 T001 `minimumReleaseAgeExclude` entries and keeps `@babel/core@7.29.6` and `yaml@2.8.3`. `29dcdc0` RS-2026-11-04-01 removes the `@swc/helpers` `0.5.23` override. A plain install left every locked version unchanged, including `@swc/helpers@0.5.23`.
- Kyle asked for a third commit after `test` failed on `node-forge@1.4.0`. `8efcf8f` pins `node-forge` to `1.4.3`. The lockfile moves only that package, from 1.4.0 to 1.4.3, for `@expo/cli` and `@expo/code-signing-certificates`.
- With the five older node-forge ignores removed, `pnpm audit --audit-level=high` passed and none of those GHSAs still appear. They are gone from `ignoreGhsas`. The other five ignores stay.
- Local lint, typecheck, and tests passed (47). GitHub `test` passed in 1m18s: https://github.com/tomale-ai-ltd/tomale-rn-test/actions/runs/43033733756/job/130567048195

## Decisions
- Kyle asked for the override on the same PR, same major, within `@expo/cli`'s `^1.4.0`, then to drop the five older node-forge ignores if 1.4.3 fixes them.
- Cursor removed GHSA-7wch-p9px-956x, GHSA-jc66-7q78-782g, GHSA-8hrf-8g6f-7xwp, GHSA-hqq3-7jhf-c5jx, and GHSA-5x38-2vff-x55p. None still apply.

## Open questions / blockers
- None. PR is not merged.

## Next
- Kyle merges #25 by rebase when ready.
