---
type: entity
entity-type: other
name: story_conversations
aliases: []
tags:
  - llm-wiki/entity
  - llm-wiki/entity/other
source-count: 3
date-updated: 2026-10-24
cssclasses: []
---


# story_conversations

## Facts

- The 'story_conversations' table is a new addition for persisting conversation history during story creation.
- Data model reused from the chatbot for tracking character creation conversations.
- Rows are created to manage conversations during story creation.

## Connections

- [[story-creation-via-chatbot]] *(part-of)*
- [[chatbot-driven-story-creation]] *(uses)*
- [[ai-assisted-child-friendly-character-builder]] *(uses)*

## Sources

- [[Project/Plan/Feature PRDs/PRD-Chatbot-Story-Conversations.md]]
- [[Project/Plan/Feature PRDs/PRD-Chatbot-Create-Character.md]]
- [[Project/Plan/2-build-plan.md]]
