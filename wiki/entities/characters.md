---
type: entity
entity-type: other
name: characters
aliases: []
tags:
  - llm-wiki/entity
  - llm-wiki/entity/other
source-count: 6
date-updated: 2026-10-24
cssclasses: []
---


# characters

## Facts

- Existing data model for character attributes including id, name, physical description, and status.
- Auth and soft delete are complete on characters as part of the API security work.
- Auth and soft delete are complete on characters as part of the Phase 1 work.
- Characters are created through a POST request and undergo content moderation.
- Included in the successful story generation run.
- characters are part of the story creation sequence in the project.

## Connections

- [[6-api-security-model]] *(part-of)*
- [[6-api-security-model]] *(related-to)*
- [[story-creation-flow]] *(applies-to)*
- [[tomale-rn-v1]] *(part-of)*
- [[tomale-rn-v1]] *(related-to)*
- [[ai-assisted-child-friendly-character-builder]] *(uses)*

## Sources

- [[Project/Plan/Feature PRDs/PRD-Chatbot-Create-Character.md]]
- [[Sessions/2026-05-07-002.md]]
- [[Sessions/2026-05-07-001.md]]
- [[Project/Architecture/story-creation-flow.md]]
- [[_raw/Chat Sessions/Untitled.md]]
- [[Sessions/2026-09-14-001.md]]
