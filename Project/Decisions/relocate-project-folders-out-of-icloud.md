---
type: decision
title: "relocate-project-folders-out-of-icloud"
project: tomale-rn-v1
status: accepted
date: 2026-10-24
related:
  - "[[knowledge-architecture]]"
  - "[[operating-model]]"
---

---

# Decision: relocate-project-folders-out-of-icloud

## What we decided

Keep iCloud Desktop & Documents sync on, but move all project working folders out of Desktop and Documents into a local, unsynced `~/Developer/tomale/` (`tomale-rn-test`, `tomale-v1-wiki`, and the new `tomale-xano` clone). Make sure files are fully downloaded before moving; update scheduled-task folders, Claude folder grants, the Cursor workspace and memory paths; retire the legacy vault and the Claude working folder.

## Why

iCloud sync is on, and the Cursor repo shows sync-conflict duplicates (including `.git/index 2` and `index 3`, and differing copies of four tab folders). Git repos inside iCloud-synced folders risk corruption, and the vault is about to become a git repo.

## Alternatives considered

Turn off iCloud Desktop & Documents sync (rejected by Kyle: wants to keep it for everything else).

## Trade-offs accepted

One-off path changes across tools. The project folders are no longer backed up by iCloud; GitHub (three private repos) plus Time Machine take over that role.

## Workflow detail

B0a in [[knowledge-architecture]] §12. Cursor diffs the `* 2` duplicates against the originals before removing them, and scans the repo before the snapshot push.

## Related notes

- [[knowledge-architecture]]
- [[operating-model]]
- [[protect-speckit-and-generated-spec-documents]]
- [[mirror-xano-workspace-to-github-read-only]]
