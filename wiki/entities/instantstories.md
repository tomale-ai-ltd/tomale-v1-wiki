---
type: entity
entity-type: other
name: instant_stories
aliases: []
tags:
  - llm-wiki/entity
  - llm-wiki/entity/other
source-count: 12
date-updated: 2026-10-24
cssclasses: []
---


# instant_stories

## Facts

- The 'instant_stories' table is used to store incremental progress of story creation with a status lifecycle.
- Draft stories are created with a status of draft.
- Auth and soft delete are complete on instant_stories as part of the API security work.
- Auth and soft delete are complete on instant_stories as part of the Phase 1 work.
- Added user_profiles_id to instant_stories.
- Parent profiles see all household stories, child profiles see only their own stories that have cleared moderation.
- The feature allows stories to be visible only to their creator profile and any parent profile on the same account.
- GET all instant_stories returns a lightweight card projection, while GET single returns a curated detailed projection.
- A story on instant_stories is visible only to the profile that created it and any parent profile on the same account.
- The flow involves creating and managing instant stories through various automated and user-triggered steps.
- A feature that allows users to create and manage stories through various API endpoints.
- instant_stories are created through a POST request and are initially set to Draft status.
- The flow covers the path from initial story creation to a story complete enough to enter the order fulfilment flow.
- Part of the story generation sequence that completed successfully.
- instant_stories is part of the story creation sequence in the project.
- The flow involves POSTing to instant_stories to create a story shell.

## Connections

- [[storydrafttags]] *(related-to)*
- [[story-creation-via-chatbot]] *(part-of)*
- [[6-api-security-model]] *(part-of)*
- [[6-api-security-model]] *(related-to)*
- [[userprofiles]] *(related-to)*
- [[userprofiles]] *(uses)*
- [[ownership-model]] *(applies-to)*
- [[visibility-model]] *(applies-to)*
- [[story-creation-flow]] *(applies-to)*
- [[tomale-rn-v1]] *(part-of)*
- [[tomale-rn-v1]] *(related-to)*
- [[chatbot-driven-story-creation]] *(uses)*
- [[tomale-rn-v1]] *(uses)*
- [[xano]] *(applies-to)*
- [[story-creation-flow]] *(applies-to)*

## Sources

- [[Project/Plan/Feature PRDs/PRD-Chatbot-Story-Conversations.md]]
- [[Project/Plan/2-build-plan.md]]
- [[Sessions/2026-05-07-002.md]]
- [[Sessions/2026-05-07-001.md]]
- [[_raw/Chat Sessions/_archive/2026-06-22-001.md]]
- [[Sessions/2026-06-22-001.md]]
- [[Project/Decisions/split-list-and-detail-projections.md]]
- [[Project/Decisions/per-child-story-visibility.md]]
- [[Project/Architecture/image-generation-flow.md]]
- [[Project/Architecture/story-creation-flow.md]]
- [[_raw/Chat Sessions/Untitled.md]]
- [[Sessions/2026-09-14-001.md]]
