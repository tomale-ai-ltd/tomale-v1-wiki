---
type: decision
title: build-image-infrastructure-in-a-claude-code-terraform-repo
project: tomale-rn-v1
status: accepted
date: 2026-11-24
related:
  - "[[2026-11-24-002]]"
affects:
  - "[[operating-model]]"
  - "[[knowledge-architecture]]"
  - "[[agent-context-sync]]"
  - "[[stack]]"
features:
  - X-process
  - X-platform
---

# Decision: build-image-infrastructure-in-a-claude-code-terraform-repo

## What we decided

- The gateway, worker, signer, eval harness and all cloud infrastructure live in a new repo, `tomale-image-gateway`, in the Tomale.ai Ltd GitHub organisation.
- Claude Code builds it, spec-first: spec-kit or `SPEC.md`, an OpenAPI contract, ADRs.
- Infrastructure is Terraform (google + aws providers) with checkov and tflint. GitHub Actions run plan, then apply after Kyle's approval, using Workload Identity Federation to both clouds.
- Kyle reviews and merges. Branch protection and a required CI check apply, as in the app repo.
- The app repo stays Cursor-only. Xano stays Kyle-only.

## Why

It keeps the new work off the app and Xano critical path, so it can run in parallel with launch work (Kyle, 24/11). Terraform makes both clouds reproducible and reviewable. Claude Code suits a code-heavy, test-driven service.

## Alternatives considered

Building inside the app repo (against the constitution's scope); click-ops in the consoles (not reproducible).

## Trade-offs accepted

- A new collaborator role and repo to govern.
- Two cloud accounts to secure.

## Workflow detail

Needs a role row in [[operating-model]] §1.2 and RACI ([[PU-2026-11-24-04]]), a `Repos/tomale-image-gateway` link in the vault, and an agent-context entry.

## Related notes

- [[IP-04-spec-contract-and-repo]]
- [[IP-08-terraform]]
