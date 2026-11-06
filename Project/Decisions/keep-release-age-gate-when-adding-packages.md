---
type: decision
title: "keep-release-age-gate-when-adding-packages"
project: tomale-rn-v1
status: accepted
date: "2026-11-05"
related:
  - "[[2026-11-05-002]]"
  - "[[promote-pnpm-migration-ahead-of-slice-100]]"
  - "[[use-expo-secure-store-for-client-tokens]]"
affects:
  - "specs/007-foundations-session/tasks.md"
features:
  - F-auth
  - X-security
---

# Decision: keep-release-age-gate-when-adding-packages

## What we decided

Kyle (05/11): do not install `expo-secure-store` by bypassing pnpm's 7-day release-age gate. T001 (add `expo-secure-store`) moves to just before T014, after 2026-11-06, and 007 implementation continues without it (MVP T002–T011, then US2 and US4 without secure storage).

## Why

Adding any package re-resolves the dependency tree, and the SDK 58 packages in the lock were still younger than the 7-day release age. Claude stopped a proposed one-off `minimumReleaseAge=0` install.

## Alternatives considered

A one-off `--config.minimumReleaseAge=0` install (rejected; the gluestack install on 04/11 had used one, [[2026-11-04-001]]).

## Trade-offs accepted

The session stays in AsyncStorage until T016, so the User Story 1 checkpoint is a test stop and must not ship; T021 depends on T016 and T019.

## Workflow detail

`package.json` and the lockfile were left unchanged and an earlier secure-store line was reverted. Cursor reorders the task list rather than bypassing the gate; the repo setting `minimumReleaseAge: 7` ([[promote-pnpm-migration-ahead-of-slice-100]], [[stack]]) is unchanged.

**Amendment (2026-11-05 evening, Kyle):** the "after 2026-11-06" date was wrong: the locked SDK 58 packages were published 03/11 and clear on 10/11. Kyle chose a narrow exception instead of waiting: [[exclude-locked-expo-sdk-versions-from-release-age-gate]]. The rule against blanket `minimumReleaseAge=0` installs stands.

## Related notes

- [[2026-11-05-002]]
- [[2026-11-04-001]]
- [[promote-pnpm-migration-ahead-of-slice-100]]
- [[use-expo-secure-store-for-client-tokens]]
- [[stack]]
