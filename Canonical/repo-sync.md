---
type: living-doc
title: repo-sync
project: tomale-rn-v1
status: current
version: 2.0
date: 2026-10-24
last_verified: 2026-11-01
owner: vault
---

# Repo sync queue

Changes to protected specs and foundations in `tomale-rn-test`, applied by a Cursor agent **only once approved**, in batches between slices, on a `repo-sync/YYYY-MM-DD` branch with one PR per batch into `main` (CI must pass). Process and classes: [[operating-model]] §3.5. Protected documents: [[knowledge-architecture]] §6.

**One note per item** in `Canonical/repo-sync/`, named by its id (since 01/11/2026; the single-file list before that is in git history). The table below is an Obsidian Base over those notes.

- **To approve:** change the item's Status cell from `queued` to `approved` (or `rejected`), in the table or in the note's properties.
- **To brief Cursor:** name the approved item ids; Cursor reads each note.
- **After Cursor applies:** set Status to `applied` and add the commit hash under "Status note" in the note.

![[repo-sync.base]]

## Item format

New items use `Templates/repo-sync-item.md`. Properties: `id` (`RS-YYYY-MM-DD-NN`, NN = next free number for that date), `title`, `status` (`queued` | `approved` | `applied` | `rejected`), `class` (`A` | `B` | `C`), `batch` (e.g. "M1, PR A"), `target`, `source`, `date`. The body holds Change, Speckit impact, Process and Verify, plus any notes.
