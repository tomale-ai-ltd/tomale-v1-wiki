---
type: decision
title: defer-postman-suite-ci-until-suite-split
project: tomale-rn-v1
status: accepted
date: 2026-10-23
related:
  - "[[knowledge-architecture]]"
---

---

# Decision: defer-postman-suite-ci-until-suite-split

## What we decided

Don't run the Postman `_tests` suite in CI yet. Later, split it into a fast, safe subset (auth, NEG, ownership) that can run anywhere, and the full order flow that runs manually and before each release, with Newman in a GitHub Action (manual trigger), ideally after dev/prod workspaces are separated.

## Why

The suite has real side effects: Stripe test sessions, Papermill PDFs and HPBC staging orders at Pureprint, plus minutes of polling. It tests the Xano backend, which isn't in GitHub, so running it on app PRs would mostly be noise. Kyle declined a paid Postman plan; Newman is free.

## Alternatives considered

Postman Monitors on a schedule (paid; creates real side effects nightly).

## Trade-offs accepted

Backend regressions are caught only by manual runs until then.

## Workflow detail

Run `_tests` manually after backend changes and before releases.

## Related notes

- [[knowledge-architecture]]
- [[2026-10-23-001]]
- [[adopt-repo-vault-ownership-split-for-project-knowledge]]
- [[adopt-tiered-vault-structure-with-canonical-folder]]
- [[adopt-frontmatter-lifecycle-schema]]
- [[generate-data-model-and-api-contract-from-xano]]
- [[add-propose-only-reconcile-and-staleness-automations]]
- [[retire-obsidian-llm-wiki-plugin]]
- [[scope-agent-context-per-tool]]
- [[version-the-vault-with-git]]
