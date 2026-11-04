---
type: decision
title: "commit-sdk-56-with-expo-doctor-exception"
project: tomale-rn-v1
status: accepted
date: "2026-11-03"
related:
  - "[[2026-11-03-002]]"
  - "[[upgrade-expo-to-sdk-58-and-use-gluestack-v5-with-uniwind]]"
  - "[[RS-2026-11-01-04]]"
affects: []
features:
  - X-platform
---

# Decision: commit-sdk-56-with-expo-doctor-exception

## What we decided

During the stepwise Expo SDK 54 → 58 upgrade (PR B, RS-2026-11-01-04), the SDK 56 commit was made with a documented `expo-doctor` exception rather than a green doctor run.

## Why

Only the known Hermes v1 regression remained at SDK 56, and it is fixed in SDK 57. The commit message links the SDK 57 changelog entry, and doctor is green at SDK 57 and 58.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

One intermediate commit on `main` does not pass `expo-doctor`; acceptable because it is never the tip and later commits are green.

## Workflow detail

Kyle approved it in PR #19 (merged by rebase 03/11; SDK 56 commit `3a090bd` on `main`).

## Related notes

- [[2026-11-03-002]]
- [[upgrade-expo-to-sdk-58-and-use-gluestack-v5-with-uniwind]]
- [[RS-2026-11-01-04]]
