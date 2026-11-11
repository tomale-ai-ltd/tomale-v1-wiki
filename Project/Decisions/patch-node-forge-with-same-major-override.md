---
type: decision
title: "patch-node-forge-with-same-major-override"
project: tomale-rn-v1
status: accepted
date: "2026-11-11"
supersedes: "[[keep-node-forge-audit-ignores-for-expo-cli]]"
related:
  - "[[2026-11-11-001]]"
  - "[[keep-node-forge-audit-ignores-for-expo-cli]]"
affects:
  - package.json (pnpm.overrides, auditConfig.ignoreGhsas)
features:
  - X-security
---

# Decision: patch-node-forge-with-same-major-override

## What we decided

Pin `node-forge` to `1.4.3` with a `pnpm.overrides` entry instead of ignoring its advisories. Expo SDK 58's CLI (`@expo/cli`, `@expo/code-signing-certificates`) asks for `^1.4.0`, so 1.4.3 is within range. The five older `node-forge` GHSA ignores are removed; the other five ignores are unchanged.

## Why

Two new high advisories (GHSA-rhr8-3pm8-cq29, GHSA-6qrw-m8cv-hcxf, published 10/11) failed CI's `pnpm audit` on PR #25. Both are fixed in `node-forge` >=1.4.1, and 1.4.3 (04/11) was past the 7-day release-age gate. Following the approved pattern (same-major overrides for highs; ignores only when the fix is a major bump or there is no fix). 1.4.3 also fixes the five advisories ignored since 01/11. `node-forge` is build tooling, not shipped in the app.

## Trade-offs accepted

One more override to drop when Expo's CLI depends on a fixed `node-forge` directly (check at the next Expo SDK update).

## Workflow detail

Applied in PR #25, `main` `acad3db` (11/11): only `node-forge` moved in the lockfile (1.4.0 → 1.4.3); audit, lint, typecheck and tests green.
