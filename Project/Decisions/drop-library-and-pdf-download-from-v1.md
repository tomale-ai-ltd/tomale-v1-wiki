---
type: decision
title: drop-library-and-pdf-download-from-v1
project: tomale-rn-v1
status: accepted
date: 2026-10-28
related:
  - "[[v1-audit]]"
affects:
  - 1-prd-tomale-react-native-app-v1
  - PRD-E-Reader
features:
  - F-bookshelf
  - F-store
---

# Decision: drop-library-and-pdf-download-from-v1

## What we decided

- **No downloadable PDFs.** Stories are read in the app's e-reader. A hard copy is obtained only by ordering a printed book. The PDFs Papermill produces are print files and are never offered to users.
- **Library is dropped from V1.**
- **Reading progress** stays in V1 only if it can be delivered without a major backend change (decided in the Slice 300 spec).

## Why

Keeps the print product valuable and trims V1 scope.

## Trade-offs accepted

No offline copy outside the app.

## Related notes

- [[v1-audit]] (P6, PRD findings)
