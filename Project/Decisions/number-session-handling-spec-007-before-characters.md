---
type: decision
title: "number-session-handling-spec-007-before-characters"
project: tomale-rn-v1
status: accepted
date: "2026-11-01"
related:
  - "[[2026-11-01-001]]"
  - "[[resume-frontend-at-slice-100]]"
  - "[[use-axios-401-interceptor-for-client-auth-session-handling]]"
affects:
  - "[[roadmap]]"
  - "[[CURRENT]]"
  - "[[v1-feature-map]]"
features:
  - F-auth
  - F-characters
  - X-process
---

# Decision: number-session-handling-spec-007-before-characters

## What we decided

PR D (client session handling) runs through speckit and takes spec 007. Characters (Slice 100) becomes 008, and the expected numbers of later features shift by one.

## Why

No script change is needed: `create-new-feature.sh` numbers each new spec as the highest existing number + 1, so the order of `/speckit.specify` runs decides the number.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Docs that name "speckit 007" for Characters need updating: [[roadmap]] M2 and the estimates table, [[CURRENT]] Next §2, [[v1-feature-map]] expected numbers, and the wording of [[resume-frontend-at-slice-100]]. Session handling (PR D) follows [[use-axios-401-interceptor-for-client-auth-session-handling]] and [[use-expo-secure-store-for-client-tokens]]; the HTTP client moves from `fetch` to Axios.

## Related notes

- [[2026-11-01-001]]
- [[resume-frontend-at-slice-100]]
- [[split-m1-into-four-ordered-cursor-prs]]
- [[name-branches-by-speckit-feature-number]]
