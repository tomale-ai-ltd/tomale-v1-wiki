---
type: decision
title: "keep-fixed-postman-inputs-in-collection-initial-values"
project: tomale-rn-v1
status: proposed
date: "2026-11-12"
related:
  - "[[2026-11-12-001]]"
affects:
  - "[[test-suite]]"
features:
  - X-testing
---

# Decision: keep-fixed-postman-inputs-in-collection-initial-values

## What we decided
Fixed Postman inputs (theme, artwork style, pages, product, shipping, story and character text) go in the collection variables' initial value so exports keep them. Tokens and passwords (and the test PIN) stay current-value only, in the environment. Claude suggested it 12/11; Kyle to confirm by doing it.

## Why
Postman exports only initial values, and importing with Replace blanks current values: after a Replace import on 12/11 Kyle had to re-enter them.

## Alternatives considered
Not discussed in session notes.

## Trade-offs accepted
The environment beats the collection, so a blank collection copy of a variable silently wins after an import if the environment lacks it.

## Workflow detail
Import with Replace, not copy. Export the collection to the vault once initial values are set.

## Related notes
[[2026-11-12-001]], [[test-suite]]
