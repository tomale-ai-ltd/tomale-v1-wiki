---
type: source
origin: user-note
date: 2026-10-22
tags:
  - llm-wiki/source
aliases: []
cssclasses: []
---


# Project/Decisions/avoid-column-named-function-inputs-in-xano.md

This document outlines a decision to avoid naming Xano function inputs or variables after columns they write to, to prevent overwriting data due to Xano's hidden-fields behavior.

## Entities

- [[tomale-v1|Tomale V1]]
- [[xano|Xano]]
- [[papermill|Papermill]]
- [[hpbc|HPBC]]
- [[pureprint|Pureprint]]

## Concepts

- [[xano-function-input-naming|Xano Function Input Naming]]
