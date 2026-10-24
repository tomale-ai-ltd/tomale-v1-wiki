---
type: source
origin: user-note
date: 2026-05-15
tags:
  - llm-wiki/source
aliases: []
cssclasses: []
---


# Project/Decisions/migrate-image-storage-to-aws-s3-signed-urls.md

This document outlines the decision to migrate image storage from Xano to AWS S3 with CloudFront, addressing privacy concerns and implementation details.

## Entities

- [[tomale-v1|Tomale V1]]
- [[xano|Xano]]
- [[aws-s3|AWS S3]]
- [[sendgrid|SendGrid]]
- [[tomale-rn-v1|Tomale-rn-v1]]
- [[cto-implementation-plan|CTO Implementation Plan]]
- [[resend|Resend]]
- [[cloudfront|CloudFront]]

## Concepts

- [[transactional-email-provider|Transactional Email Provider]]
- [[image-storage-migration|Image Storage Migration]]
- [[signed-urls|Signed URLs]]
