---
type: decision
title: fix-rs-06-with-targeted-speckit-and-gitignore-changes
project: tomale-rn-v1
status: accepted
date: 2026-10-29
related:
  - "[[2026-10-29-001]]"
  - "[[2026-10-28-002]]"
  - "[[repo-sync]]"
affects:
  - "[[repo-sync]]"
  - ".cursor/commands/speckit.*"
  - ".gitignore"
features:
  - X-process
---

# Decision: fix-rs-06-with-targeted-speckit-and-gitignore-changes

## What we decided

Repo-sync item RS-06 in the app repo (`tomale-rn-test`) is handled as a targeted fix rather than a wider repo restructure: three speckit command path fixes, `.cursor/` now tracked in git, and `.gitignore` hardened.

## Why

Not discussed in session notes.

## Alternatives considered

- A wider repo restructure.
- Upgrading speckit (the 28/10 session framed RS-06 as "upgrade speckit or a one-line fix", pending Kyle's decision).

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Cursor made the edits and Claude reviewed them. Merged as PR #10, rebase-merged into the `wip/` branch. Follow-up repo-sync items RS-2026-10-29-01/02/03 were added (optional micro-PRD input for `/speckit.specify`, `update-agent-context.sh` sed escaping, `.gitignore` hardening). This clears the RS-06 dependency for B10 repo sync.

## Related notes

- [[2026-10-29-001]]
- [[2026-10-28-002]]
- [[repo-sync]]
- [[protect-speckit-and-generated-spec-documents]]
- [[follow-knowledge-architecture-stage-order-before-slice-100]]
- [[knowledge-architecture]]
