---
type: entity
entity-type: tool
name: AsyncStorage
aliases: []
tags:
  - llm-wiki/entity
  - llm-wiki/entity/tool
source-count: 6
date-updated: 2026-10-24
cssclasses: []
---


# AsyncStorage

## Facts

- AsyncStorage is actively used as the persistence backend for Zustand via `createJSONStorage`.
- It is the standard persistence layer for lightweight client state in this architecture.
- The package used is `@react-native-async-storage/async-storage`.
- Frontend token storage is managed via AsyncStorage.
- Auth persists across launches via AsyncStorage with hydration guard before route decisions.
- Used for JWT-based authentication storage.
- AsyncStorage is the persistence layer for auth tokens, preferences, and lightweight data.
- The current stack-doc position was to keep tokens in AsyncStorage.

## Connections

- [[zustand]] *(uses)*
- [[tomale-rn-v1]] *(uses)*
- [[zustand]] *(related-to)*
- [[xano]] *(related-to)*
- [[zustand]] *(uses)*
- [[jwt-based-authentication]] *(uses)*
- [[expo-secure-store]] *(contrasts-with)*

## Sources

- [[Project/Stack/9. AsyncStorage.md]]
- [[Project/Stack/7. Auth - Xano.md]]
- [[Project/Stack/5. State Management - Zustand.md]]
- [[Project/Stack/1. Overview.md]]
- [[Project/Cursor/constitution.md]]
- [[Project/Decisions/use-expo-secure-store-for-client-tokens.md]]
