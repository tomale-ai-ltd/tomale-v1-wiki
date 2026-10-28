---
type: decision
title: adopt-modified-semver-versioning
project: tomale-rn-v1
status: accepted
date: 2025-12-27
features:
  - X-process
---

# Decision: Adopt Modified SemVer Versioning

## What we decided

Follow Semantic Versioning (SemVer) with a project-specific mapping that
aligns version increments with Expo's OTA vs app store release distinction:

- `major` — fundamental application rewrites (likely v1.x.x for a long time)
- `minor` — app store required updates (native code changes or new permissions)
- `patch` — over the air (OTA) updates via Expo Updates

## Why

Standard SemVer (breaking / feature / fix) doesn't map cleanly onto mobile
app release constraints. The most operationally significant distinction for
Tomale is whether a change requires app store re-submission or can be shipped
as an OTA update.

Mapping `minor` to store submissions and `patch` to OTA creates a version
number that communicates release type to users and the team at a glance —
a user on v1.2.3 being prompted to upgrade to v1.3.0 understands a meaningful
new submission is involved.

## Alternatives considered

- **Standard SemVer (breaking / feature / fix)** — rejected: doesn't reflect
  the operational reality of mobile app releases where the native/JS
  distinction matters more than the API breaking change distinction
- **Build numbers only** — rejected: opaque to users and harder to reason
  about in support and rollback scenarios

## Trade-offs accepted

- `major` version will stay at 1 for a long time — less meaningful than in
  a library context
- Team must be disciplined about correctly classifying changes as OTA vs
  store-required

## Consequences

- Every release must be classified as OTA (patch) or store submission (minor)
  before branching
- CI/CD check should enforce OTA eligibility where possible
- Expo release channels map to version types:
  - `dev` — feature development
  - `staging` — current head of main
  - `production` — latest store release


**Amendment (2026-10-28, B7 audit):** date approximate. The original note carried a placeholder date (2025-01-01); 2025-12-27 is the CTO tech review period it came from.

## Related notes

- [[trunk-based-git-branching]]
- [[12. CICD - EAS, GitHub]]
- [[3-cto-tech-review]]