---
type: foundation
title: sdd-flow
status: current
project: tomale-rn-v1
date: 2026-04-14
---

___
## Overview

This document describes the spec-driven development workflow used for all V1 feature work. Every feature is broken into Slices, each Slice into Sub-Slices, and each Sub-Slice follows a strict specify → plan → clarify → implement loop before any code is written. 

--- 
## Top-level flow 

1. **Project Setup Tasks** 

— one-time setup before slice work begins 

2. **Slice Setup Tasks** 

— preparation work done at the start of each slice 

3. **Slices** (000, 100, 200…) 

— major feature divisions, worked through in sequence 

4. **End** 

— project complete when all slices are done 
Slices repeat until all are complete. 

--- 
## Sub-Slice workflow 

Each Slice contains multiple Sub-Slices (e.g. 101, 102, 103, 104). Every Sub-Slice follows this loop: 
### 1. Specify 

Write the spec for the sub-slice. 

- **Pass checks? 
- NO** → return to Specify and revise 
- **Pass checks? 
- YES** → proceed to Plan 
### 2. Plan 

Plan the implementation approach for the sub-slice. 

- Feeds into Clarify 
### 3. Clarify 

Clarify any ambiguities or open questions in the plan. 

- **Changes required? 
- YES** → return to Plan - **Changes required? 
- NO** → proceed to Tasks 
### 4. Tasks 

Break the clarified plan into discrete implementation tasks. 
### 5. Analyze 

Review the tasks for completeness and correctness. 

- **Changes required? 
- YES** → return to Plan - **Changes required? 
- NO** → proceed to Implement 
### 6. Implement 

Execute the tasks. 

Implementation only begins once the spec, plan, and analysis have all passed without required changes. 

---
## Key principles

- No implementation begins until Specify → Plan → Clarify → Analyze have all passed 
- The loop back to Plan from both Clarify and Analyze ensures implementation is always based on a fully resolved spec 
- Sub-Slices within a Slice can be worked through in parallel or sequence depending on dependencies 
 
----
## Related notes 

- [[constitution]] 
- [[sdd-process-overview]] 
- [[2-build-plan]]