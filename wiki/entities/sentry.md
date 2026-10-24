---
type: entity
entity-type: tool
name: Sentry
aliases: []
tags:
  - llm-wiki/entity
  - llm-wiki/entity/tool
source-count: 9
date-updated: 2026-10-24
cssclasses: []
---


# Sentry

## Facts

- Sentry is used for error tracking and basic observability on the React Native frontend.
- Implement Source Maps + Debug Symbols.
- Enrich events with anonymized user identifier.
- Set up Tracing + Profiling.
- Integrate Sentry into React Native app (backend if feasible via Xano hooks).
- Used for logging and alerting, with recommendations for implementation.
- Sentry is used for crash reporting with privacy-preserving tools and PII scrubbing enabled.
- Sentry is used for tracking captured events including app crashes and runtime exceptions.
- Sentry is used for monitoring captured events including app crashes and runtime exceptions.
- Crash reporting MUST use privacy-preserving tools (e.g., Sentry) with PII scrubbing enabled.
- Sentry is used for crash reporting with PII scrubbing enabled.
- Sentry is used for monitoring and logging application behavior.
- Backend error reporting must be built manually using Sentry's event endpoint.
- Sentry is used for observability and logging within the project.

## Connections

- [[react-native]] *(uses)*
- [[xano]] *(related-to)*
- [[logging-alerting]] *(part-of)*
- [[security]] *(uses)*
- [[logging-alerting]] *(uses)*
- [[observability]] *(uses)*
- [[backend-observability]] *(uses)*
- [[tomale-rn-v1]] *(uses)*
- [[xano]] *(contrasts-with)*
- [[tomale]] *(uses)*

## Sources

- [[Project/Stack/15. Observability - Sentry.md]]
- [[Project/Plan/4-cto-improvements-list.md]]
- [[Project/Plan/5-cto-implementation-plan.md]]
- [[Project/Plan/3-cto-tech-review.md]]
- [[Project/Cursor/constitution.md]]
- [[Project/Plan/6-api-security-model.md]]
- [[Sessions/2026-05-12-001.md]]
- [[Project/Decisions/elevate-backend-observability-to-launch-requirement.md]]
- [[Project/Plan/documentation-refresh-backlog.md]]
