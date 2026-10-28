---
type: decision
title: name-branches-by-speckit-feature-number
project: tomale-rn-v1
status: accepted
date: 2026-10-28
supersedes:
  - "[[trunk-based-git-branching]]"
related:
  - "[[v1-audit]]"
  - "[[adopt-spec-driven-development]]"
affects:
  - tomale-rn-test branches
  - constitution
features:
  - X-process
---

# Decision: name-branches-by-speckit-feature-number

## What we decided

The trunk-based model stays: a protected `main` (PR required, linear history, squash or rebase), short-lived branches, and release branches later. Only the naming changes to match practice:

- Features: `NNN-short-name`, created by `/speckit.specify` (e.g. `007-characters`).
- Repo maintenance: `repo-sync/<topic>` (batched repo-sync items).
- One-off restructure or tooling work: a short descriptive branch (e.g. `b6/generated-specs`), merged by PR.
- `wip/` branches only as temporary snapshots, resolved into `main` and deleted.
- `release/A.B.x` for store releases and OTA cherry-picks, as in the original note, once releases start.

## Why

The old `feat/XXX-description` naming was never used; speckit names feature branches itself.

## Alternatives considered

Rename speckit branches to `feat/…`: rejected, because speckit relies on the `^[0-9]{3}-` pattern.

## Trade-offs accepted

None material.

## Related notes

- [[v1-audit]] (C3)
- [[adopt-modified-semver-versioning]]
- [[upgrade-github-org-to-team-for-main-protection]]
