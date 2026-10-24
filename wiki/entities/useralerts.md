---
type: entity
entity-type: other
name: user_alerts
aliases: []
tags:
  - llm-wiki/entity
  - llm-wiki/entity/other
source-count: 7
date-updated: 2026-10-24
cssclasses: []
---


# user_alerts

## Facts

- The user_alerts endpoint work has started, with the GET all functionality completed.
- Endpoints for user alerts were closed and new internal functions were built.
- User alerts endpoints were closed and an internal function for notifications was built.
- Work on the user_alerts endpoint has started, with the GET all endpoint completed.
- The user_alerts group was closed, and the first alert-injection call sites were wired.
- The user_alerts feature was started, with GET all complete.
- The user_alerts will utilize a nullable action_url text column for deep-linking.
- Scoped as an in-app inbox, distinct from push notifications.
- Its public surface is READ + mark-read only; creation is internal-only via a create_user_alert() function.
- The in-app user_alerts inbox reaches 100% of active users and covers the V1 notification need on its own.

## Connections

- [[content-moderation]] *(applies-to)*
- [[notificationscreateuseralert]] *(uses)*
- [[api-security-model]] *(applies-to)*
- [[actionurl-deep-linking]] *(uses)*
- [[in-app-inbox]] *(part-of)*
- [[userprofiles]] *(related-to)*
- [[tomale]] *(part-of)*
- [[tomale-rn-v1]] *(part-of)*
- [[userprofiles]] *(related-to)*
- [[tomale-rn-v1]] *(uses)*

## Sources

- [[_raw/Chat Sessions/_archive/2026-07-02-001.md]]
- [[_raw/Chat Sessions/_archive/2026-06-30-001.md]]
- [[Sessions/2026-07-02-001.md]]
- [[Sessions/2026-06-30-001.md]]
- [[Project/Decisions/use-action-url-for-user-alert-deep-linking.md]]
- [[Project/Decisions/scope-user-alerts-as-in-app-inbox.md]]
- [[Project/Decisions/defer-push-notifications-until-post-v1.md]]
