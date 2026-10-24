---
type: decision
title: "promote-pnpm-migration-ahead-of-slice-100"
project: tomale-rn-v1
status: accepted
date: 2026-10-24
related:
  - "[[5-cto-implementation-plan]]"
  - "[[knowledge-architecture]]"
affects:
  - "[[5-cto-implementation-plan]]"
  - constitution
  - package.json
  - CI
---

---

# Decision: promote-pnpm-migration-ahead-of-slice-100

## What we decided

Move the npm → pnpm migration (CTO plan §5.1–5.3, scheduled as Phase 5 item 27, "non-critical path") forward so it's done **after the pre-restructure repo snapshot and before the frontend resumes at Slice 100**. It's one piece of repo work covering:
- pnpm with install scripts blocked by default, allowing only the packages that need them;
- `minimumReleaseAge: 7`;
- `pnpm audit` in CI, failing on high and critical;
- review of the 49 `npm audit` findings (5 low, 15 moderate, 26 high, 3 critical, 24/10), measuring real exposure with dev-only dependencies excluded.

## Why

§5.1's rationale is a security one ("no auto script execution"): npm runs every package's install scripts automatically, which is how 2025's npm supply-chain worms spread. Doing it before Slice 100 means all frontend work runs on the safer setup, and the vulnerability fixes are made once against the new lock file.

## Alternatives considered

Keep it in Phase 5 as planned (rejected: leaves the install-script exposure in place through all of V1 frontend work). Do it during the snapshot (rejected: the snapshot must capture the repo exactly as it is).

## Trade-offs accepted

A lock-file and CI change before Slice 100; some Expo/React Native packages may need explicit allowance for their build scripts.

## Workflow detail

Done by a Cursor agent on its own branch, through a `repo-sync` item (class B, plus a class A constitution amendment if the constitution's tooling standards name npm), with Kyle reviewing. Don't run `npm audit fix` (especially `--force`) in the meantime.

## Related notes

- [[5-cto-implementation-plan]]
- [[classify-and-batch-repo-sync-changes]]
- [[protect-speckit-and-generated-spec-documents]]
