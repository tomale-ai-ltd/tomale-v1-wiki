---
type: decision
title: trunk-based-git-branching
project: tomale-rn-v1
status: accepted
date: 2025-01-01
---

---

# Decision: Adopt Trunk-Based Git Branching Model

## What we decided

Use trunk-based development with `main` as the default branch and short-lived
feature and release branches.

Three branch types:
- `feat/XXX-description` — feature development, merged into main
- `release/A.B.X` — app store releases, branched from main
- OTA patches cherry-picked from main onto current release branch

## Why

As a solo developer using spec-driven development with AI assistance, a simple
and consistent branching model reduces cognitive overhead and prevents
accidental releases. Trunk-based development keeps the main branch always
releasable and avoids long-lived branches diverging.

The model also directly supports the OTA vs app store release distinction —
a critical operational concern for an Expo-based app where the release type
determines whether a re-submission is required.

## Alternatives considered

- **Gitflow** — rejected: designed for teams with parallel release streams,
  adds unnecessary complexity for a solo project
- **No formal branching model** — rejected: ad hoc branching led to unclear
  release state during early development

## Trade-offs accepted

- Cherry-picking for OTA patches requires care to avoid conflicts
- Short-lived branches require discipline to keep PRs small

## Workflow detail

### New feature

1. Checkout `feat/ABC-description` from `main`
2. Develop using spec-driven process
3. Open PR; CI/CD checks pass
4. CI/CD determines OTA or store submission required
5. Merge into `main`, delete branch

### App store release

1. Branch `release/1.2.X` from `main`
2. Run release job; increment version numbers
3. Submit to app stores
4. Tag `v1.2.0` on approval

### OTA release

1. Checkout `feat/DEF-description` from `main`
2. Develop; CI/CD approves for OTA
3. Cherry-pick onto current release branch
4. Run OTA release job targeting `production` Expo channel
5. Tag `v1.2.1`

## Consequences

- All feature work starts from `main` — no long-lived feature branches
- CI must be blocking on `main` merges
- Release branches are maintained until superseded by the next minor release
- OTA eligibility is determined by CI/CD check (no native code changes,
  no new permissions)

## Related notes

- [[3-cto-tech-review]]
- [[adopt-modified-semver-versioning]]
- [[12. CICD - EAS, GitHub]]