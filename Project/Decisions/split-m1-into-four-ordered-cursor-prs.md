---
type: decision
title: "split-m1-into-four-ordered-cursor-prs"
project: tomale-rn-v1
status: accepted
date: "2026-11-01"
related:
  - "[[2026-11-01-001]]"
  - "[[m1-cursor-briefs]]"
affects:
  - "[[roadmap]]"
features:
  - X-process
  - X-platform
---

# Decision: split-m1-into-four-ordered-cursor-prs

## What we decided

M1 (app foundations rework) goes to Cursor as four PRs, in order:
- **A** tooling/CI (Node 22 first; Renovate; Gitleaks + Semgrep in the `test` job; repo-sync Cursor rule).
- **B** Expo SDK 58 + constitution 1.6.0.
- **C** `app.config.js` + gluestack-ui v5.
- **D** client session handling (via speckit, 007).

Cursor stops at an open PR; Kyle merges (rebase), and Claude records the main-branch hashes against the repo-sync items after merge.

## Why

Not discussed in session notes, beyond the dependency order: SDK 58 needs Node ≥ 22.13, so PR A lands first.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Prompts for each PR are in [[m1-cursor-briefs]]. PR A merged 01/11 (PR #15). Kyle approved the PR B items (RS-2026-11-01-04, -01, -06, RS-2026-10-30-04).

## Related notes

- [[2026-11-01-001]]
- [[m1-cursor-briefs]]
- [[upgrade-expo-to-sdk-58-and-use-gluestack-v5-with-uniwind]]
- [[number-session-handling-spec-007-before-characters]]
