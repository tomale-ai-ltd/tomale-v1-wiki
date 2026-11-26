---
type: decision
title: "track-cloud-budgets-on-gross-spend"
project: tomale-rn-v1
status: accepted
date: "2026-11-26"
related:
  - "[[2026-11-26-001]]"
  - "[[gateway-constitution-draft]]"
  - "[[image-pipeline-plan]]"
affects:
  - "[[PRD-Image-Pipeline]]"
  - gateway constitution 1.0.0 (tomale-image-gateway)
features:
  - X-platform
---

# Decision: track-cloud-budgets-on-gross-spend

## What we decided

Cloud budgets exclude Savings (credits), so alerts track real usage (gross spend) rather than the net bill after credits. Recorded in the 26/11 session; the gateway constitution Kyle approved the same day says budgets with alerts at 25/50/75% "MUST exist on both clouds, tracking spend before credits" ([[gateway-constitution-draft]]).

## Why

So that alerts track real usage: with credits applied the net spend stays near zero and a budget would never fire.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

GCP project `tomale-image-dev`: budget £400 on all services, with Savings cleared (26/11). The billing account is in GBP; the credits are $25k GCP and $10k AWS. The same rule applies to the AWS budget when it is set up.

## Related notes

[[2026-11-26-001]], [[gateway-constitution-draft]], [[image-pipeline-plan]], [[PRD-Image-Pipeline]]
