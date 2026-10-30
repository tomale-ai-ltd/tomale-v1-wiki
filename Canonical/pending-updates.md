---
type: living-doc
title: pending-updates
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-10-24
last_verified: 2026-10-24
owner: vault
---

# Pending updates

Proposed edits to canonical docs, from the daily pipeline's reconcile step, the weekly staleness check, or Claude in session. **Kyle approves; Claude applies** and bumps `version` / `last_verified`. See [[operating-model]] §3.4.

Format:
```
### PU-YYYY-MM-DD-NN: <short title>
- Target: [[doc]]
- Proposed change: <what and why>
- Source: [[decision or session]]
- Status: proposed | approved | applied | rejected
```

### PU-2026-10-30-01: Knowledge architecture §10–11 and open questions after B11
- Target: [[knowledge-architecture]]
- Proposed change: §10 automations table: daily knowledge pipeline runs at 17:40 weekdays (not 17:00) and the weekly staleness check on Mondays 10:17; step 5 syncs `Canonical/`, all decisions, the constitution and the data model using the hash manifest `Project/Automation/project-sync-manifest.json` (not only "changed Canonical docs and new decisions"). A scheduled task was tested in B11 and can write Project knowledge, so drop the fallback sentence under the table and close open question 1 (§14). §11 Claude chat row: Project knowledge also holds the constitution and data model. Summary line "one 17:00 automation pipeline" → 17:40.
- Source: [[sync-project-knowledge-by-hash-manifest]], [[2026-10-30-001]]
- Status: applied (approved by Kyle 30/10)

### PU-2026-10-30-02: Agent context sync, Project knowledge row
- Target: [[agent-context-sync]]
- Proposed change: Claude Project knowledge row: drop "(or at session start if a scheduled task can't write Project knowledge)", since B11 confirmed it can; name the hash manifest as the mechanism.
- Source: [[sync-project-knowledge-by-hash-manifest]], [[2026-10-30-001]]
- Status: applied (approved by Kyle 30/10)

### PU-2026-10-30-03: Operating model §0, data-model conflict resolved
- Target: [[operating-model]]
- Proposed change: §0 "Known conflict to resolve in B10" (constitution said to edit `data-model.md` by hand) was resolved by constitution 1.5.0 (RS-2026-10-24-01, PR #11, 29/10). Replace with a dated note that it is resolved, and write the command as `pnpm run update:datamodel` (pnpm since constitution 1.5.1).
- Source: [[subordinate-operating-model-to-constitution]], [[2026-10-30-001]]
- Status: applied (approved by Kyle 30/10)

