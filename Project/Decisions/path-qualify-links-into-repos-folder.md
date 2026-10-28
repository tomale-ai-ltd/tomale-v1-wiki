---
type: decision
title: path-qualify-links-into-repos-folder
project: tomale-rn-v1
status: accepted
date: 2026-10-24
related:
  - "[[2026-10-24-001]]"
  - "[[adopt-tiered-vault-structure-with-canonical-folder]]"
  - "[[protect-speckit-and-generated-spec-documents]]"
affects:
  - "[[knowledge-architecture]]"
---

# Decision: path-qualify-links-into-repos-folder

## What we decided

Vault links stay `[[filename]]` only, with one exception: links into `Repos/` are path-qualified (e.g. `[[Repos/tomale-rn-test/memory/constitution|constitution]]`). Added to [[knowledge-architecture]] §8.

## Why

Speckit generates the same filenames (research, data-model, contracts, quickstart, plus spec, plan and tasks) in every feature folder, so filename-only links into the repo views would be ambiguous.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

In B4, 235 path-style links were rewritten to filename links, with links into `Repos/` kept path-qualified. No vault note may reuse the speckit filenames.

## Related notes

- [[2026-10-24-001]]
- [[knowledge-architecture]]
- [[adopt-tiered-vault-structure-with-canonical-folder]]
- [[protect-speckit-and-generated-spec-documents]]
- [[adopt-frontmatter-lifecycle-schema]]
