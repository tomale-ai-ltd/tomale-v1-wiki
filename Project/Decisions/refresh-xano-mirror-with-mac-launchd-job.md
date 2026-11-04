---
type: decision
title: "refresh-xano-mirror-with-mac-launchd-job"
project: tomale-rn-v1
status: accepted
date: "2026-11-03"
related:
  - "[[2026-11-03-001]]"
  - "[[mirror-xano-workspace-to-github-read-only]]"
  - "[[keep-agents-out-of-xano-no-mcp]]"
affects:
  - "[[knowledge-architecture]]"
features:
  - X-process
  - X-security
---

# Decision: refresh-xano-mirror-with-mac-launchd-job

## What we decided

Refresh the local Xano mirror (`tomale-xano`) with a launchd job on Kyle's Mac rather than giving an agent GitHub credentials. The job `ai.tomale.xano-pull` runs `git pull --ff-only` in `tomale-xano` at 17:30 on weekdays using Kyle's own GitHub access. Source: `Project/Automation/ai.tomale.xano-pull.plist`; log: `~/Library/Logs/tomale-xano-pull.log`.

## Why

The daily pipeline's shell has no GitHub credentials, so its mirror refresh step always failed. Kyle's GitHub login can push to every repo, which is too broad a scope to hand to an unattended agent.

## Alternatives considered

- Give the scheduled task's shell Kyle's GitHub login: rejected on scope (push access to every repo).
- A read-only deploy key: rejected because the key would sit in an agent-readable folder.
- Manual pulls only.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

The job was loaded and tested on 03/11; the mirror moved from the 24/10 to the 30/10 sync. Applied in session to [[knowledge-architecture]] 1.3 §10, which also says to still `git pull` by hand before a backend review if Xano was published since 17:30. The daily pipeline's own pull will keep failing without credentials; the launchd job is now the refresh path.

## Related notes

- [[2026-11-03-001]]
- [[mirror-xano-workspace-to-github-read-only]]
- [[keep-agents-out-of-xano-no-mcp]]
- [[knowledge-architecture]]
