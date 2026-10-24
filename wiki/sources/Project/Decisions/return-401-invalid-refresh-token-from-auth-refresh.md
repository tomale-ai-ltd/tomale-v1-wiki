---
type: source
origin: user-note
date: 2026-10-22
tags:
  - llm-wiki/source
aliases: []
cssclasses: []
---


# Project/Decisions/return-401-invalid-refresh-token-from-auth-refresh.md

This document outlines the decision to modify the `auth/refresh` endpoint to return a 401 status for invalid or reused refresh tokens, along with the rationale and implications of this change.

## Entities

- [[tomale-rn-v1|Tomale-rn-v1]]
- [[6-api-security-model|6-api-security-model]]
- [[postman|Postman]]

## Concepts

- [[401-invalid-refresh-token-response|401 Invalid Refresh Token Response]]
