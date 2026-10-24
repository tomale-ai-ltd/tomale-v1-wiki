---
type: decision
title: create-architecture-folder-for-system-flow-docs
date: 2026-07-15
status: current
project: tomale-rn-v1
---

---

# Decision: create-architecture-folder-for-system-flow-docs

## What we decided

A new `Project/Architecture/` folder was established to hold system-flow documentation and function contracts (e.g. `order-fulfilment-flow.md`, a Mermaid flowchart of the full order lifecycle produced this session). Function internals stay out of this folder and remain in XanoScript comments where they self-check against the real implementation.

## Why

Established during a documentation-strategy discussion on Obsidian, RAG, and where different documentation artifacts belong. System flows and function contracts are high-value and low-drift, worth authoring and maintaining as standalone docs. Function internals are low-value and high-drift as separate documentation — best left in code comments, where reality checks them directly. Documentation effort is best spent on the why (decisions) and the seams (system flows), which code cannot hold on its own.

## Alternatives considered

Documenting function internals as standalone markdown alongside or instead of code comments — rejected as high-drift and low-value relative to the effort.

## Trade-offs accepted

Not discussed in session notes beyond the value/drift rationale.

## Workflow detail

`Project/Architecture/order-fulfilment-flow.md` is the first artifact in the new folder. The broader documentation direction (keeping the vault as plain markdown with rich wikilinks and consistent frontmatter, naming functions by their exact names in prose, treating any generated `Wiki/` layer as rebuildable output, and not yet building a RAG/knowledge-graph layer) was discussed but not committed as a separate decision this session — captured as a future-direction item in the session note's scratchpad.

## Related notes

[[Sessions/2026-07-15-001]]
[[order-fulfilment-flow]]
