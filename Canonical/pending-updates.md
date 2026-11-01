---
type: living-doc
title: pending-updates
project: tomale-rn-v1
status: current
version: 2.0
date: 2026-10-24
last_verified: 2026-11-01
owner: vault
---

# Pending updates

Proposed edits to canonical docs, from the daily pipeline's reconcile step, the weekly staleness check, or Claude in session. **Kyle approves; Claude applies** and bumps `version` / `last_verified`. See [[operating-model]] §3.4.

**One note per item** in `Canonical/pending-updates/`, named by its id (since 01/11/2026). The table below is an Obsidian Base over those notes.

- **To approve:** change the item's Status cell from `proposed` to `approved` (or `rejected`).
- **After Claude applies:** Status → `applied`.

![[pending-updates.base]]

## Item format

New items use `Templates/pending-update.md`. Properties: `id` (`PU-YYYY-MM-DD-NN`, NN = next free number for that date), `title`, `status` (`proposed` | `approved` | `applied` | `rejected`), `target` (the doc as a wikilink), `source`, `date`. The body holds the proposed change.
