---
type: decision
title: version-the-vault-with-git
project: tomale-rn-v1
status: accepted
date: 2026-10-23
related:
  - "[[knowledge-architecture]]"
---

---

# Decision: version-the-vault-with-git

## What we decided

Put the vault under git in a private GitHub repo `tomale-v1-wiki`, with the Obsidian Git community plugin for automatic commit and pull. Day to day, commit straight to `main`; each restructure stage runs on a branch with a PR diff reviewed on GitHub. Ignore `.obsidian/workspace*`, `.DS_Store`, `.trash/`, `*.bak-*`. The vault and the Cursor repo stay separate repos and never nest; `Repo/` symlinks are committed as links.

## Why

It gives every change, by Kyle, Claude or an automation, a reviewable diff and a rollback, which matters most during the restructure and for automation output.

## Alternatives considered

Ad hoc `.bak` copies (the current practice; no history, clutter).

## Trade-offs accepted

One-off setup; pushing needs Kyle's GitHub login (GitHub Desktop).

## Workflow detail

Review automation and Claude edits as diffs. `.bak` copies are no longer needed once git is in place.

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
- [[defer-postman-suite-ci-until-suite-split]]
