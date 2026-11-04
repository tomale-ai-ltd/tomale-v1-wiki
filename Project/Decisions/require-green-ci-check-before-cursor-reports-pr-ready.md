---
type: decision
title: "require-green-ci-check-before-cursor-reports-pr-ready"
project: tomale-rn-v1
status: proposed
date: "2026-11-04"
related:
  - "[[2026-11-04-001]]"
  - "[[operating-model]]"
affects:
  - "[[operating-model]]"
  - "`.cursor/rules/tomale-project.mdc`"
features:
  - X-process
  - X-testing
---

# Decision: require-green-ci-check-before-cursor-reports-pr-ready

## What we decided

Cursor must always confirm the GitHub `test` check has passed before reporting a PR ready.

## Why

CI failed twice on PR #20 (`TS2882` for `import "@/global.css"`) although Cursor reported typecheck passing: locally the CSS module declaration came from the gitignored `expo-env.d.ts`, which CI doesn't have.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Cursor was told this in session on 04/11; later Cursor notes report the `test` result (e.g. "CI `test` passed on `fc7681f`"). `gh pr checks` is on the repo allowlist.

## Related notes

- [[2026-11-04-001]]
- [[operating-model]]
