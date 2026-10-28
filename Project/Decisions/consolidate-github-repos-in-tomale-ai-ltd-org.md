---
type: decision
title: consolidate-github-repos-in-tomale-ai-ltd-org
project: tomale-rn-v1
status: accepted
date: 2026-10-24
related:
  - "[[2026-10-24-001]]"
  - "[[upgrade-github-org-to-team-for-main-protection]]"
features:
  - X-process
---

# Decision: consolidate-github-repos-in-tomale-ai-ltd-org

## What we decided

The GitHub organisation was renamed `tomale-ai-dev` → `tomale-ai-ltd` and holds every Tomale repo: `tomale-rn-test`, `tomale-v1-wiki` and `tomale-xano`. `tomale-ai` stays as Kyle's login and the org owner. Unused repos were deleted and VELA moved out.

## Why

The rename avoids a clash with Xano's "dev". Not otherwise discussed in session notes.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Every remote and the Xano sync URL had to be updated. While being repointed, the Xano sync briefly targeted `tomale-rn-test` and pushed three commits to `main`; reverted with a force-with-lease push to `507a26f`.

## Workflow detail

All remotes and the Xano sync URL point at `tomale-ai-ltd`. Org deploy keys are enabled; Xano syncs only to `tomale-xano`, and Xano's deploy key was removed from `tomale-rn-test`.

## Related notes

- [[2026-10-24-001]]
- [[upgrade-github-org-to-team-for-main-protection]]
- [[mirror-xano-workspace-to-github-read-only]]
- [[version-the-vault-with-git]]
- [[separate-dev-prod-environments]]
- [[knowledge-architecture]]
