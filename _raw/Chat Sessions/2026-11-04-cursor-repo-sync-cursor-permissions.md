---
date: 2026-11-04
source: cursor
branch: repo-sync/2026-11-04-cursor-permissions
feature: RS-2026-11-04-03
---

# Repo allowlist and deny hook for Cursor commands

## What changed
- Commit `ed5ea0795f5237cbacb346a570c5f60f8bfdc241` on `repo-sync/2026-11-04-cursor-permissions`. PR https://github.com/tomale-ai-ltd/tomale-rn-test/pull/21 (not merged). CI check `test` passed.
- `.cursor/permissions.json` sets `terminalAllowlist` only (no `mcpAllowlist`, no `autoRun`).
- `.cursor/hooks.json` runs `.cursor/hooks/guard.sh` on `beforeShellExecution` with `failClosed: true`. Other commands print `{}`.

## Decisions
- Kyle approved RS-2026-11-04-03. Cursor kept one commit and did not merge.
- Cursor also denies `git push` refspecs that start with `+` and the short `-d` delete flag, because those are force-push and delete. `--force-with-lease` still returns no decision.
- Cursor ignores heredoc bodies, so a commit or PR message that mentions a blocked command is not itself blocked. `$(git push --force …)` and `bash -lc "…"` still deny.

## Open questions / blockers
- `pnpm add left-pad` did not prompt. Run Mode was already Allowlist, and the sandbox auto-ran it (`allCommandsAllowlisted: false`). The install failed on `minimumReleaseAge` and did not change tracked files. With the sandbox on, Allowlist mode asks only when the command cannot stay in the sandbox.

## Next
- Kyle reviews PR 21 and merges by rebase. Cursor does not update the repo-sync item status.
