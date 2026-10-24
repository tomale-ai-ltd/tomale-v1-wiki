---
type: decision
title: "adopt-order-of-authority-for-project-knowledge"
project: tomale-rn-v1
status: accepted
date: 2026-10-24
related:
  - "[[knowledge-architecture]]"
  - "[[operating-model]]"
---

---

# Decision: adopt-order-of-authority-for-project-knowledge

## What we decided

When sources disagree, the higher one wins: (1) the live system (published Xano / its mirror; app code); (2) protected and generated specs; (3) canonical docs; (4) accepted decisions; (5) session notes; (6) raw notes, research, archive. New knowledge rises along the promotion path: raw note → session note → decision → canonical doc or protected spec. A conflict between levels is a defect, fixed by correcting the lower source or deliberately changing the higher one.

## Why

This week showed agents and docs disagreeing with the live system (stale data model, AsyncStorage tokens, an outdated security matrix). A fixed precedence tells agents what to trust and makes drift visible.

## Alternatives considered

No explicit precedence (the status quo).

## Trade-offs accepted

Agents must state which source they relied on when sources disagree.

## Workflow detail

Used by every agent; diagrams in [[knowledge-architecture]] §3.

## Related notes

- [[knowledge-architecture]]
- [[operating-model]]
- [[add-propose-only-reconcile-and-staleness-automations]]
- [[adopt-frontmatter-lifecycle-schema]]
- [[adopt-repo-vault-ownership-split-for-project-knowledge]]
- [[adopt-tiered-vault-structure-with-canonical-folder]]
- [[defer-postman-suite-ci-until-suite-split]]
- [[generate-data-model-and-api-contract-from-xano]]
- [[keep-agents-out-of-xano-no-mcp]]
- [[mirror-xano-workspace-to-github-read-only]]
- [[protect-speckit-and-generated-spec-documents]]
- [[retire-obsidian-llm-wiki-plugin]]
- [[scope-agent-context-per-tool]]
- [[version-the-vault-with-git]]
