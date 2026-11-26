---
type: decision
title: "use-no-service-account-keys-on-gcp"
project: tomale-rn-v1
status: accepted
date: "2026-11-26"
related:
  - "[[2026-11-26-001]]"
  - "[[gateway-constitution-draft]]"
  - "[[build-image-infrastructure-in-a-cursor-terraform-repo]]"
affects:
  - "[[PRD-Image-Pipeline]]"
  - gateway constitution 1.0.0 (tomale-image-gateway)
features:
  - X-security
  - X-platform
---

# Decision: use-no-service-account-keys-on-gcp

## What we decided

No service account keys, now or in Terraform: people use Application Default Credentials (ADC), CI and services use Workload Identity Federation (WIF). The gateway constitution Kyle approved on 26/11 says the same and adds that service account keys and AWS access keys MUST NOT be created ([[gateway-constitution-draft]]).

## Why

Not discussed in session notes.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

On 26/11 gcloud was set up with an ADC login and quota project on `tomale-image-dev`; Kyle has Owner, so no extra roles were needed. GitHub Actions reach both clouds through WIF ([[build-image-infrastructure-in-a-cursor-terraform-repo]]).

## Related notes

[[2026-11-26-001]], [[gateway-constitution-draft]], [[build-image-infrastructure-in-a-cursor-terraform-repo]], [[PRD-Image-Pipeline]]
