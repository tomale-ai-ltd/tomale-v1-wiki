---
type: decision
title: classify-and-batch-repo-sync-changes
project: tomale-rn-v1
status: accepted
date: 2026-10-24
related:
  - "[[knowledge-architecture]]"
  - "[[operating-model]]"
features:
  - X-process
---

# Decision: classify-and-batch-repo-sync-changes

## What we decided

Repo sync is a controlled change process. Items in `Canonical/repo-sync.md` use a fixed format (id, class, target, change, source decision, speckit impact, process, verify, status). Class A (governance: the constitution) follows the constitution's own amendment rules (`/speckit.constitution`, Sync Impact Report, semver, PR with migration notes, Kyle's approval as document owner, then `/speckit.analyze` on active specs). Class B (agent rules) goes through a Cursor edit and PR. Class C (generated specs) runs the script. speckit tool files are never changed by repo sync. Items need approval before they're applied, are applied in batches on a `repo-sync/` branch between slices, and are ticked off with a commit hash after verification.

## Why

Changes to protected specs can change how speckit works and how Cursor builds; an informal queue risked changing rules under an in-flight slice or bypassing the constitution's governance.

## Alternatives considered

A simple checklist applied ad hoc (rejected: too loose for files that drive the spec-driven flow).

## Trade-offs accepted

Slower turnaround for spec changes; batches wait for a gap between slices (except class C).

## Workflow detail

[[operating-model]] §3.5. `tomale-project.mdc` is itself a class B target, kept in step with the operating model's Cursor sections.

## Related notes

- [[knowledge-architecture]]
- [[operating-model]]
- [[protect-speckit-and-generated-spec-documents]]
- [[mirror-xano-workspace-to-github-read-only]]
