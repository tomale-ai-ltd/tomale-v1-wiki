---
date: 2026-11-04
source: cursor
branch: repo-sync/2026-11-04-cursor-permissions
feature: RS-2026-11-04-03
---

# Guard now asks before sandbox-auto-run writes

## What changed
- Amended `ed5ea079` to `fc7681fb8281302ea43439a061f49b13b64466ad` and force-pushed with `--force-with-lease` to PR https://github.com/tomale-ai-ltd/tomale-rn-test/pull/21. Not merged.
- `guard.sh` still denies merge, force push, push to main, remote delete, and eas submit/update. It now returns `ask` for dependency changes, any other git push, gh pr create, eas build, git reset/rebase/clean, rm -rf, curl, and wget.

## Decisions
- Kyle asked for the amend and the lease force-push. Cursor kept a single commit.
- `pnpm install --frozen-lockfile` still returns no decision so the allowlist can run it. `pnpm install` without that flag asks.
- `--force-with-lease` asks. `--force` and `-f` still deny.

## Open questions / blockers
- `pnpm add left-pad` and `git push --force-with-lease` both raised approval cards (`hook_forces_prompt`). The approval gate then allowed both. The install failed on `minimumReleaseAge` and did not change tracked files. The lease push updated the PR branch.

## Next
- CI `test` passed on `fc7681f` (57s). Kyle reviews and merges. Cursor does not update the repo-sync item status.
