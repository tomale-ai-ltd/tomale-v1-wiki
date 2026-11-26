---
type: decision
title: build-image-infrastructure-in-a-cursor-terraform-repo
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

# Decision: build-image-infrastructure-in-a-cursor-terraform-repo

## What we decided

- The gateway, worker, signer, eval harness and all cloud infrastructure live in a new repo, `tomale-image-gateway`, in the Tomale.ai Ltd GitHub organisation.
- **Cursor agents build it** (changed 26/11, Kyle: same models, an established workflow, no IDE switch), spec-first with speckit, an OpenAPI contract and ADRs.
- Infrastructure is Terraform (google + aws providers) with checkov and tflint. GitHub Actions run plan, then apply after Kyle's approval, using Workload Identity Federation to both clouds.
- Kyle reviews and merges. Branch protection and a required CI check apply, as in the app repo.
- The repo copies the rn-test agent guard rails (`.cursor/permissions.json` allowlist and `guard.sh` hook), adding cloud rules: `terraform plan` allowed; `terraform apply`/`destroy` and any mutating `gcloud`, `aws` or `gsutil` command denied or asked; no credentials in the repo. Xano stays Kyle-only.

## Why

It keeps the new work off the app and Xano critical path, so it can run in parallel with launch work (Kyle, 24/11). Terraform makes both clouds reproducible and reviewable. Cursor already has a proven, guarded workflow on this project; using Claude Code would add a second tool for no gain (first proposed 24/11, replaced 26/11).

## Alternatives considered

Building inside the app repo (against the constitution's scope); click-ops in the consoles (not reproducible).

## Trade-offs accepted

- A second repo for Cursor's rules and guard to cover.
- Two cloud accounts to secure.

## Workflow detail

Needs the Cursor role in [[operating-model]] §1.2 extended to a second repo ([[PU-2026-11-24-04]]), a `Repos/tomale-image-gateway` link in the vault, and an agent-context entry.

## Related notes

- [[IP-04-spec-contract-and-repo]]
- [[IP-08-terraform]]
