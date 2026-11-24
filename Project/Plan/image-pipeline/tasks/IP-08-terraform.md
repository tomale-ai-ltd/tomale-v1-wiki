---
type: plan-task
id: IP-08
title: "Terraform for GCP and AWS"
status: todo
owner: "Claude Code"
depends:
  - "[[IP-04-spec-contract-and-repo]]"
  - "[[IP-01-credits-and-accounts]]"
gate: ""
effort_days: 3
target: 2026-12-09
scoping: full-spec
project: tomale-rn-v1
---

# IP-08: Terraform for GCP and AWS

**Goal:** GCP: Cloud Run gateway and worker, Cloud Tasks queue with rate caps, Secret Manager, service accounts, Workload Identity Federation, monitoring and budgets. AWS: private S3, CloudFront with OAC and key group, Lambda signer with function URL, Rekognition IAM, OIDC trust for the Cloud Run service account, CloudWatch and budgets. GitHub Actions plan/apply with approval.

**Done when:** checkov and tflint clean; `terraform plan` reviewed by Kyle; dev environment applied; nothing public in S3 (Access Analyzer).

**Notes:** Dev and prod as separate workspaces from the start.

Plan: [[image-pipeline-plan]] · Scope: [[PRD-Image-Pipeline]]
