---
type: source
origin: user-note
date: 2026-07-02
tags:
  - llm-wiki/source
aliases: []
cssclasses: []
---


# Project/Decisions/prevent-deleting-active-profile-via-soft-delete.md

This document outlines a decision to implement a soft-delete mechanism for user profiles, preventing the deletion of the currently active profile to avoid broken-token states.

## Entities

- [[tomale-rn-v1|Tomale-rn-v1]]

## Concepts

- [[soft-delete-mechanism|soft-delete mechanism]]
