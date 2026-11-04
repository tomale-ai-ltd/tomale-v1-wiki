---
type: decision
title: "enforce-cursor-permissions-with-repo-allowlist-and-guard-hook"
project: tomale-rn-v1
status: accepted
date: "2026-11-04"
related:
  - "[[2026-11-04-001]]"
  - "[[RS-2026-11-04-03]]"
affects:
  - "[[operating-model]]"
  - "`.cursor/permissions.json`"
  - "`.cursor/hooks.json`"
  - "`.cursor/hooks/guard.sh`"
features:
  - X-process
  - X-security
---

# Decision: enforce-cursor-permissions-with-repo-allowlist-and-guard-hook

## What we decided

Cursor's command permissions for `tomale-rn-test` are set in the repo, not in each machine's Settings:

- A committed `.cursor/permissions.json` with a `terminalAllowlist` of exact command prefixes (never bare `git`, `pnpm`, `npx` or `gh`). It replaces the Settings command list for this repo; no `mcpAllowlist` and no `autoRun` block.
- A fail-closed `beforeShellExecution` hook (`.cursor/hooks/guard.sh`) that hard-denies merges (`gh pr merge`), force pushes (`--force`, `-f`, `+` refspecs), pushes to `main`, remote branch deletes (`--delete`, `-d`, `:branch`), `eas submit` and `eas update`, and forces approval ("ask") for dependency changes, any other `git push` (including `--force-with-lease`), `gh pr create`, `eas build`, `git reset`/`rebase`/`clean`, `rm -rf`, `curl` and `wget`.
- `pnpm install --frozen-lockfile` stays allowlisted; non-frozen `pnpm install` asks. Heredoc bodies are ignored, so a commit or PR message that mentions a blocked command is not blocked; `$(…)` and `bash -lc "…"` wrappers still deny.

## Why

Kyle merges and approves supply-chain changes. Run Mode alone let sandboxed commands through: with the sandbox on, Allowlist mode auto-ran a non-allowlisted `pnpm add`, so "ask" has to be enforced by the hook.

## Alternatives considered

Relying on Cursor Settings and Run Mode (Allowlist) alone: shown during verification not to prompt for sandboxable commands. Not otherwise discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Applied in PR #21 (`8339e23`, rebase-merged 04/11) as RS-2026-11-04-03. Kyle trimmed risky entries from his Settings allowlist (`git push`, `python3`, `node`, `.`, `command`, `cd`, `set`, `npm install`, `pnpm install`, `corepack`). Verified: allowlisted commands run silently; denies hold even when a command is allowlisted; `pnpm add` and `git push --force-with-lease` raise approval cards.

## Related notes

- [[2026-11-04-001]]
- [[RS-2026-11-04-03]]
- [[operating-model]]
