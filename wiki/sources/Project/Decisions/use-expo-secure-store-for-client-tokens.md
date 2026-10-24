---
type: source
origin: user-note
date: 2026-10-22
tags:
  - llm-wiki/source
aliases: []
cssclasses: []
---


# Project/Decisions/use-expo-secure-store-for-client-tokens.md

This document outlines the decision to store client authentication tokens in `expo-secure-store` instead of AsyncStorage, resolving a conflict in the stack documentation regarding client authentication.

## Entities

- [[asyncstorage|AsyncStorage]]
- [[tomale-rn-v1|Tomale-rn-v1]]
- [[expo-secure-store|expo-secure-store]]

## Concepts

- [[future-hardening-decision|future hardening decision]]
