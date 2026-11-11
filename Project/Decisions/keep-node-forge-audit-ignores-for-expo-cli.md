---
type: decision
title: "keep-node-forge-audit-ignores-for-expo-cli"
project: tomale-rn-v1
status: superseded
date: "2026-11-03"
related:
  - "[[2026-11-03-002]]"
  - "[[RS-2026-11-01-06]]"
affects: []
superseded_by: "[[patch-node-forge-with-same-major-override]]"
features:
  - X-security
---

# Decision: keep-node-forge-audit-ignores-for-expo-cli

## What we decided

When removing PR A's one-off audit exceptions (RS-2026-11-01-06), keep the five `node-forge` GHSA ignores. The `follow-redirects` exclude and override were removed.

## Why

Expo SDK 58's CLI still resolves `node-forge@1.4.0`; removing the ignores makes `pnpm audit --audit-level=high` fail.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Five known `node-forge` advisories stay ignored in the audit gate until the Expo CLI moves off that version.

## Workflow detail

Decided by Cursor while applying RS-2026-11-01-06 in PR #19 (commit `9421916` on `main`, merged by Kyle 03/11).

## Related notes

- [[2026-11-03-002]]
- [[RS-2026-11-01-06]]
