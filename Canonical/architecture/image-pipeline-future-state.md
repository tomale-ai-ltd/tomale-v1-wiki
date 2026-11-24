---
type: architecture
title: image-pipeline-future-state
aliases:
  - Image Pipeline Future State
project: tomale-rn-v1
status: draft
version: 0.1
date: 2026-11-24
last_verified: 2026-11-24
owner: vault
related:
  - "[[image-generation-flow]]"
  - "[[PRD-Image-Pipeline]]"
  - "[[image-pipeline-research-2026-11]]"
scope: As-is and target image pipeline across Xano, Google Cloud and AWS
---

# Image pipeline: as-is and future state

Draft for [[PRD-Image-Pipeline]]. [[image-generation-flow]] stays the record of what's live, and is rewritten from this note at cut-over (IP-16).

## As-is (after Session 0)

```mermaid
flowchart LR
  App["React Native app"] -->|create story| ORCH["Xano orchestrator_story_images"]
  ORCH --> JOBS[("image_jobs: queued")]
  TICK["image_worker_tick (every 5 min)"] -->|claim + lease| JOBS
  TICK --> EXE["Executors: cover / page / character<br/>(async-shared pool, effectively serial)"]
  EXE --> DM[("data_models<br/>page, cover: default record<br/>character: record pinned on the character")]
  EXE --> GPT["OpenAI gpt-4o-mini<br/>prompt compiler (ends 14/01/2027)"]
  EXE --> OIMG["OpenAI images API<br/>gpt-image-2.6-flare, text-only prompt<br/>(character: edits with portrait)"]
  EXE --> XFS[("Xano public file storage")]
  EXE --> CHK["story_completion_check"]
  App -->|public image URLs| XFS
  TTS["Xano create_tts_audio<br/>gpt-4o-mini-tts (ends 06/01/2027)"] -->|service-account key| GCS[("GCS bucket: audio")]
```

**Limits:**
- The 5-minute tick and serial pool give 10–15 minutes per book.
- Page and cover images get no reference picture.
- No output image moderation.
- Public URLs.
- Paid in cash.

## Future state

```mermaid
flowchart LR
  subgraph APP["Client"]
    RN["React Native app"]
  end
  subgraph XANO["Xano (two batched sessions of changes)"]
    API["app endpoints<br/>create story, get story"]
    ORCH["orchestrator_story_images<br/>dispatches the whole book at once"]
    JOBS[("image_jobs: queued / dispatched / complete / error")]
    TICK["image_worker_tick<br/>reaper, kill switch, safety net"]
    EXE["Executors: provider = tomale_gateway → POST job"]
    HOOK["webhooks: image_jobs callback (HMAC, idempotent)"]
    CHK["story_completion_check"]
    DM[("data_models: gateway records + OpenAI fallback record")]
  end
  subgraph GCP["Google Cloud (credits)"]
    GW["Cloud Run gateway (europe-west2)"]
    CT["Cloud Tasks queue<br/>rate + concurrency caps"]
    WK["Cloud Run worker (scales to zero)"]
    LLM["Gemini 3.1 Flash-Lite (eu)<br/>compiler + VLM judge"]
    IMG["Gemini 3.1 Flash Image (eu)<br/>labelled character + style refs"]
    SM["Secret Manager"]
    MON["Cloud Monitoring + budgets"]
  end
  subgraph AWS["AWS eu-west-2 (credits)"]
    S3[("S3 private bucket")]
    CF["CloudFront + OAC<br/>1-hour signed URLs"]
    SIG["Lambda URL signer"]
    REK["Rekognition moderation labels"]
    CW["CloudWatch + budgets"]
  end
  OAI["OpenAI gpt-image-2.6 (fallback, cash)"]
  RN -->|create / get story| API
  API --> ORCH --> JOBS
  TICK --> JOBS
  ORCH --> EXE
  TICK --> EXE
  EXE --> DM
  EXE -->|POST batch| GW --> CT --> WK
  WK --> LLM
  WK --> IMG
  WK -.->|fallback provider| OAI
  WK -->|OIDC web identity| S3
  WK --> REK
  WK -->|result + s3 key| HOOK --> JOBS
  HOOK --> CHK
  WK --> SM
  WK --> MON
  API -.->|sign URLs for a story| SIG
  RN -->|fetch images| CF
  SIG -.-> CF
  CF --> S3
  S3 --> CW
```

The app still reads image URLs from Xano. Xano asks the signer for a story's URLs in one call, so it never holds the CloudFront private key.

## One book, 13 images in parallel

```mermaid
sequenceDiagram
  participant App
  participant Xano
  participant GW as Cloud Run gateway
  participant CT as Cloud Tasks
  participant WK as Worker
  participant V as Vertex Gemini (eu)
  participant AWS as S3 + Rekognition
  App->>Xano: Create story
  Xano->>Xano: 13 image_jobs (cover + 12 pages)
  Xano->>GW: POST /v1/batches (13 jobs, HMAC)
  GW->>CT: Enqueue 13 tasks (name = job id + attempt)
  GW-->>Xano: 202 Accepted (jobs → dispatched)
  par up to the queue's concurrency cap
    CT->>WK: Job k
    WK->>V: Compile prompt (Flash-Lite, JSON schema)
    WK->>V: Generate (labelled refs + style ref)
    WK->>AWS: Rekognition check
    WK->>V: VLM judge (guidelines, attributes, bleed)
    WK->>AWS: PUT story/page-k.png
    WK->>Xano: Callback complete (s3 key, usage, verdict)
  end
  Xano->>Xano: story_completion_check → Done
  App->>Xano: Get story
  Xano->>AWS: Signer (13 URLs)
  App->>AWS: Images via CloudFront
```

**Expected timing** (to confirm in the load test): compile 2–5 s, generate 10–40 s, moderation 3–6 s. That's about a minute per book with no queueing. Under load, the Cloud Tasks queue behind dynamic quota is what stretches it.

## Failure paths

- **Retryable** (429, 5xx, provider safety finish with a softened prompt): Cloud Tasks retries with backoff. On the final attempt the worker posts `error_retry` or `error_terminal`.
- **Callback lost:** the job stays `dispatched` until its lease expires, then the reaper requeues it. The idempotent task name stops double generation within a retry window.
- **Rollback:** set the OpenAI fallback record as the default for that type. Jobs in flight finish through the callback.
