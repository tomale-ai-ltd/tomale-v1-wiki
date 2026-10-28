---
type: decision
title: use-xano-branches-for-dev-and-prod
project: tomale-rn-v1
status: accepted
date: 2026-10-28
supersedes:
  - "[[separate-dev-prod-environments]]"
related:
  - "[[v1-audit]]"
  - "[[knowledge-architecture]]"
affects:
  - knowledge-architecture
  - Xano workspace
  - tomale-xano
features:
  - X-platform
---

# Decision: use-xano-branches-for-dev-and-prod

## What we decided

Dev and prod are two Xano **branches** in one workspace (Launch plan), not separate instances. Work is published on dev many times; at release dev is merged into prod and prod is published once. Each branch syncs to its own git branch in `tomale-xano`. Branches can point at different data sources. Where an environment variable differs between dev and prod, it is duplicated with a suffix (e.g. `api_key_test`), which matches how the backend is already built.

## Why

Easier to work across branches and move changes between them in Xano, fits the current plan and a later upgrade, and is what [[knowledge-architecture]] §9 already assumes.

## Alternatives considered

Separate Xano instances (the original note): stronger isolation of data and env vars, but duplicated workspace setup and manual promotion of every change.

## Trade-offs accepted

Dev and prod share one workspace's settings and env-var namespace, so suffixed variables need care: a wrong suffix could point dev at a live key. Covered by the pre-launch checklist.

## Related notes

- [[v1-audit]] (C2)
- [[mirror-xano-workspace-to-github-read-only]]
- [[key-hpbc-environment-switch-off-stripe-test-mode]]
