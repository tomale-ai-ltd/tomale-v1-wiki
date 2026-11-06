---
type: decision
title: "exclude-locked-expo-sdk-versions-from-release-age-gate"
project: tomale-rn-v1
status: accepted
date: "2026-11-05"
related:
  - "[[2026-11-05-003]]"
  - "[[keep-release-age-gate-when-adding-packages]]"
  - "[[use-expo-secure-store-for-client-tokens]]"
affects:
  - "pnpm-workspace.yaml (minimumReleaseAgeExclude)"
  - "specs/007-foundations-session/tasks.md (T001)"
features:
  - F-auth
  - X-security
---

# Decision: exclude-locked-expo-sdk-versions-from-release-age-gate

## What we decided

To install `expo-secure-store` (007 T001) on 06/11, add the **exact versions already in the lockfile** that are younger than 7 days to `minimumReleaseAgeExclude` in `pnpm-workspace.yaml`, one `name@version` entry each with a comment. The gate itself (`minimumReleaseAge: 10080`) stays on; nothing other than `expo-secure-store` and what it strictly needs may be added or upgraded. The entries are removed once they pass 7 days ([[RS-2026-11-05-06]]).

## Why

Kyle (05/11): "We need to move forward with the build. We can always reverse this once we're in a stable state." The blocking packages are the Expo SDK 58 set (`expo` 58.0.23, `expo-router` 58.0.30, `@expo/cli` 58.1.19 and others) published 03/11 around 17:00 UTC and already installed and in use since 04/11; they clear the gate on 10/11 about 17:10 UTC. `expo-secure-store` 58.0.2 was published 01/10. So the exception lets in nothing new except the package we chose.

## Alternatives considered

- Wait until 10/11 evening: delays US3, device tests and PR D by about three working days.
- A one-off `minimumReleaseAge=0` install: rejected on 05/11 ([[keep-release-age-gate-when-adding-packages]]); it would let any young version in.

## Trade-offs accepted

A short-lived, explicit exception to the release-age rule for already-locked versions. Same pattern as the Renovate security excludes.
