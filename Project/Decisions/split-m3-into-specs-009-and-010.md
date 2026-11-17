---
type: decision
title: "split-m3-into-specs-009-and-010"
project: tomale-rn-v1
status: accepted
date: "2026-11-17"
related:
  - "[[2026-11-17-001]]"
  - "[[roadmap]]"
affects:
  - "[[roadmap]]"
  - "[[v1-feature-map]]"
features:
  - F-profiles
  - F-parental-oversight
  - X-process
---

# Decision: split-m3-into-specs-009-and-010

## What we decided
M3's app work runs as two speckit features: **009 profiles and PIN** (picker, switching, PIN pad and lock, set/change PIN, manage profiles, header avatar for every profile), then **010 approvals** (parent inbox, review and approve/reject, child waiting card). Later slices shift by two: story creation 011, bookshelf and e-reader 012, store 013, AI character creation 014 (Kyle, 17/11).

## Why
Smaller specs and PRs; 010 depends on 009's PIN gate and profile switching, so profiles go first.

## Alternatives considered
One spec for all of M3 (one large PR); suffixed numbers (008a/008b) to avoid renumbering.

## Trade-offs accepted
Roadmap and feature-map spec numbers change for M4 onwards.
