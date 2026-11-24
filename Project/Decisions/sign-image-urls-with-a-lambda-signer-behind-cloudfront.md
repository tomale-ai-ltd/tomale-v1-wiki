---
type: decision
title: "sign-image-urls-with-a-lambda-signer-behind-cloudfront"
project: tomale-rn-v1
status: proposed
date: "2026-11-24"
related:
  - "[[2026-11-24-002]]"
  - "[[migrate-image-storage-to-aws-s3-signed-urls]]"
affects:
  - "[[migrate-image-storage-to-aws-s3-signed-urls]]"
  - "[[security-model]]"
  - "[[pre-launch-checklist]]"
  - "GET /instant_stories, GET /instant_stories/{id}, characters reads"
features:
  - X-security
  - F-story-generation
  - F-characters
---

# Decision: sign-image-urls-with-a-lambda-signer-behind-cloudfront

## What we decided

Refines [[migrate-image-storage-to-aws-s3-signed-urls]]:
- Generated images go to a private S3 bucket in eu-west-2 (Block Public Access, encryption at rest), served through CloudFront with Origin Access Control and 1-hour signed URLs.
- A small Lambda signer (function URL, HMAC-authenticated) returns signed URLs for a whole story in one call. Xano calls it on story and character reads, so Xano never holds the CloudFront private key or does RSA signing.
- The gateway writes to S3 with AWS STS web-identity federation from its Google service account. No AWS keys are stored in GCP.

## Why

It meets the accepted signed-URL decision without asking Xano to do RSA signing, and keeps the key in AWS. It's paid from AWS credits.

## Alternatives considered

Signing inside Xano (key in env vars, unproven RSA support); GCS with Cloud CDN signed URLs (contradicts the AWS London decision); Xano private files (rejected before).

## Trade-offs accepted

- One extra call per story read (batched).
- The client must handle URL expiry, already planned in the original decision.

## Workflow detail

- New images land in S3 from the cut-over.
- Backfilling existing images, and user-uploaded images, stay with the M9 signed-URL task.

## Related notes

- [[migrate-image-storage-to-aws-s3-signed-urls]]
- [[image-pipeline-future-state]]
