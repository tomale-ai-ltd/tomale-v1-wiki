---
type: decision
title: upgrade-github-org-to-team-for-main-protection
project: tomale-rn-v1
status: accepted
date: 2026-10-24
related:
  - "[[2026-10-24-001]]"
  - "[[consolidate-github-repos-in-tomale-ai-ltd-org]]"
features:
  - X-process
---

# Decision: upgrade-github-org-to-team-for-main-protection

## What we decided

The `tomale-ai-ltd` GitHub organisation was upgraded to the Team plan so `main` branch protection is enforced. The `tomale-rn-test` rule moves to a ruleset: approvals 0, no force pushes, restricted deletions, squash/rebase merges.

## Why

The constitution requires `main` protection, and enforcement needed the Team plan.

## Alternatives considered

Amending the constitution to drop or soften the requirement (rejected in favour of the upgrade).

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

`main` on `tomale-rn-test` can't be force-pushed or deleted; changes land through squash or rebase merges.

## Related notes

- [[2026-10-24-001]]
- [[consolidate-github-repos-in-tomale-ai-ltd-org]]
- [[trunk-based-git-branching]]
- [[protect-speckit-and-generated-spec-documents]]
- [[Repos/tomale-rn-test/memory/constitution|constitution]]
