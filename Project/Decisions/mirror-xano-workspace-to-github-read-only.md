---
type: decision
title: mirror-xano-workspace-to-github-read-only
project: tomale-rn-v1
status: accepted
date: 2026-10-24
related:
  - "[[knowledge-architecture]]"
  - "[[operating-model]]"
features:
  - X-process
---

# Decision: mirror-xano-workspace-to-github-read-only

## What we decided

Turn on Xano's GitHub sync to a private repo `tomale-xano`. Every sync commits the published XanoScript; Git is read-only from Xano's side (building and publishing stay in Xano). A local clone is exposed read-only in the vault as `Repos/tomale-xano/` and pulled by the daily pipeline. It replaces the staged `.xs` files in the Claude working folder. Turned on in B0, after a full Xano backup, so its first commit is the pre-restructure baseline.

## Why

The backend had no readable source of truth outside Xano, so agents reviewed pasted or stale copies (a stale `auth/login` draft nearly reintroduced user enumeration on 22/10). The mirror gives version history, rollback reference, off-platform backup of code, and a reliable thing to diff Xano AI drafts against.

## Alternatives considered

Keep staging `.xs` files by hand in the working folder (rejected: stale copies). Xano CLI pull/push (not needed for read-only review).

## Trade-offs accepted

Available on the Launch plan. Each Xano branch syncs to its own git branch: with the V1 dev/prod split, many publishes on dev give many dev commits; release is a Xano merge dev → prod plus one prod publish, giving one prod commit. Mirrors code, not data; data stays covered by Xano backups and exports.

## Workflow detail

Backend reviews compare drafts with the mirror's current file. Session notes link to the mirror commit for each backend change.

## Related notes

- [[knowledge-architecture]]
- [[operating-model]]
- [[add-propose-only-reconcile-and-staleness-automations]]
- [[adopt-frontmatter-lifecycle-schema]]
- [[adopt-order-of-authority-for-project-knowledge]]
- [[adopt-repo-vault-ownership-split-for-project-knowledge]]
- [[adopt-tiered-vault-structure-with-canonical-folder]]
- [[defer-postman-suite-ci-until-suite-split]]
- [[generate-data-model-and-api-contract-from-xano]]
- [[keep-agents-out-of-xano-no-mcp]]
- [[protect-speckit-and-generated-spec-documents]]
- [[retire-obsidian-llm-wiki-plugin]]
- [[scope-agent-context-per-tool]]
- [[version-the-vault-with-git]]
