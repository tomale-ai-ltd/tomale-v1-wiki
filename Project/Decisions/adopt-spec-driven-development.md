---
type: decision
title: adopt-spec-driven-development
date: 2025-10-01
status: current
project: tomale-rn-v1
---
# Decision: Adopt Spec-Driven Development

## What we decided

All V1 feature work follows a spec-driven development process. No implementation
begins until a sub-slice has passed through Specify → Plan → Clarify → Analyze
without requiring further changes.

## Why

Building with LLM assistance (Cursor/Claude) creates a specific risk: it's very
easy to generate plausible-looking code quickly, but without a locked spec the
LLM will make assumptions that compound into architectural drift over time.
Spec-driven development forces ambiguity to be resolved before code is written,
not during or after.

Secondary reasons:

- Solo project with no second reviewer — the spec loop acts as a forcing function
  that replaces the review process a team would provide
- Xano backend + React Native frontend have a clear contract boundary — specs
  define that contract explicitly before either side is built
- Easier to course-correct a spec than refactor implemented code

## Alternatives considered

- **Ad-hoc development** — rejected because LLM-assisted ad-hoc work tends to
  produce inconsistent patterns across features with no single source of truth
- **Test-driven development** — considered but requires more upfront test
  infrastructure than is practical for a solo V1 build at this stage

## Trade-offs accepted

- Slower to start on any given feature — the spec loop adds time before first
  line of code
- Requires discipline to not skip the loop when a feature feels simple or obvious

## Consequences

- Every feature has a PRD in [[plan/Feature PRDs/]] before work begins
- Cursor constitution and process overview enforce this at the tooling level
- Session notes should reference which sub-slice is in progress and what stage
  of the loop it's at

## Related notes

- [[Repos/tomale-rn-test/memory/constitution|Constitution]]
- [[sdd-process-overview]]
- [[sdd-flow]]
- [[2-build-plan]]