---
type: architecture
title: image-generation-flow
aliases:
  - Image Generation Flow
project: tomale-rn-v1
status: draft
version: 1.0
date: 2026-08-04
last_verified: 2026-08-04
owner: vault
related:
  - "[[story-creation-flow]]"
scope: orchestrator_story_images through worker tick to the three async executors
---

# Image Generation Flow

Documents the image generation pipeline from the orchestrator that queues jobs, through the scheduled worker tick that claims and dispatches them, to the three async executors that generate the images.

This is a subprocess of [[story-creation-flow]] step 9.

## Diagram

```mermaid
flowchart TD
    subgraph ORCH["orchestrator_story_images"]
        O1["fires at end of<br/>generate_story_page_text"] --> O2["create image_jobs"]
        O2 --> O3["1 cover-image job<br/>N page-image jobs"]
        O3 --> O4["each job set:<br/>status = queued<br/>priority (cover higher)<br/>attempt = 0<br/>max_attempts from env"]
    end

    O4 --> TICK

    subgraph TICK["image_worker_tick (scheduled)"]
        direction TB
        T0["kill switch<br/>image_workers_enabled"] --> TR

        subgraph TR["Recovery and concurrency"]
            TR1["find stuck jobs<br/>status = processing<br/>AND locked_until <= now - grace"] --> TR2["requeue: status = error_retry<br/>priority +10<br/>release lease<br/>(does NOT increment attempt)"]
            TR2 --> TR3["count running jobs<br/>status = processing<br/>AND locked_until > now"]
        end

        TR --> TH{"running >= max_running?"}
        TH -->|"yes"| TSTOP["throttle: stop this tick"]
        TH -->|"no"| DRAIN

        subgraph DRAIN["Drain loop (max_loops times)"]
            D1["run claim_image_jobs<br/>batch_size"] --> D2{"claimed count > 0?"}
            D2 -->|"no"| DBREAK["break loop"]
            D2 -->|"yes"| D3["for each claimed job"]
            D3 --> D4["attempt = attempt + 1"]
            D4 --> D5{"attempt > max_attempts?"}
            D5 -->|"yes"| D6["status = error_terminal<br/>continue to next job"]
            D5 -->|"no"| D7["write attempt to image_jobs"]
            D7 --> D8{"job_type?"}
            D8 -->|"cover-image"| DC["dispatch executor_cover_image<br/>async-shared"]
            D8 -->|"page-image"| DP["dispatch executor_page_image<br/>async-shared"]
            D8 -->|"character-image"| DCH["dispatch executor_character_image<br/>async-shared"]
            DC --> D9["add executor_runs row<br/>status = queued<br/>async_job_id, created_at"]
            DP --> D9
            DCH --> D9
        end
    end

    subgraph CLAIM["claim_image_jobs"]
        CL1["query image_jobs<br/>locked_until <= now<br/>AND retry_at <= now<br/>AND status in (queued, error_retry)"] --> CL2["sort priority desc,<br/>created_at asc<br/>limit batch_size"]
        CL2 --> CL3["for each: set status = processing<br/>locked_until = now + lease_seconds"]
        CL3 --> CL4["return claimed job ids"]
    end

    D1 -.calls.-> CLAIM

    D9 --> EXEC

    subgraph EXEC["Async executors (one per job_type)"]
        direction TB
        E1["get image_jobs row"] --> E2["find own executor_runs row<br/>by image_jobs_id + created_at"]
        E2 --> E3["set started_at<br/>extend locked_until = now + lease_seconds"]
        E3 --> E4["load data_models<br/>(default active, by type)"]
        E4 --> E5["prompt compiler<br/>build prompt from story,<br/>page or character, characters"]
        E5 --> E6["text model call<br/>(structured JSON out)"]
        E6 --> E7["image model call<br/>gpt-image-1"]
        E7 --> E8{"api_status?"}
        E8 -->|"200"| E9["upload image to storage<br/>write to target record<br/>record token_usage"]
        E9 --> E10["image_jobs: status = complete<br/>release lease"]
        E10 --> E11["executor_runs: status = success<br/>whitelisted api_request/response"]
        E8 -->|"retryable<br/>429, 5xx, 408"| E12["image_jobs: status = error_retry<br/>priority +10, retry_at backoff"]
        E8 -->|"fatal<br/>4xx"| E13["image_jobs: status = error_terminal"]
        E12 --> E14["executor_runs: status = error"]
        E13 --> E14
    end

    E11 --> DONE{"story complete?"}
    DONE -->|"page executor:<br/>recount pages without images<br/>set images_remaining"| SC["story_completion_check"]
    DONE -->|"cover executor:<br/>write cover_image"| SC
    SC --> FIN["images_remaining = 0<br/>status = Done"]

    classDef executor fill:#ffffff,stroke:#1a4d8f,stroke-width:3px,color:#000000
    classDef problem fill:#ffffff,stroke:#000000,stroke-width:2px,stroke-dasharray:4 3,color:#000000
    class DC,DP,DCH executor
    class TR2,E12,E13 problem

    style ORCH fill:none,stroke:#666666,stroke-dasharray:5 4
    style TICK fill:none,stroke:#666666,stroke-dasharray:5 4
    style TR fill:none,stroke:#999999,stroke-dasharray:3 3
    style DRAIN fill:none,stroke:#999999,stroke-dasharray:3 3
    style CLAIM fill:none,stroke:#666666,stroke-dasharray:5 4
    style EXEC fill:none,stroke:#666666,stroke-dasharray:5 4
```

Blue bordered nodes dispatch the async executors. Dashed black bordered nodes are the state transitions involved in the duplication and retry logic under investigation.

## The correlation key

The executor finds its own `executor_runs` row using `image_jobs_id` plus `created_at` as a compound key (step E2). This depends on `created_at` being immutable. If anything rewrites `created_at` after the row is created, this lookup can match the wrong row or match ambiguously, which is a live suspect in the duplication investigation.

## Lease lifecycle

The lease (`locked_until`) is the mechanism that stops two ticks claiming the same job:

1. `claim_image_jobs` sets `locked_until = now + lease_seconds` when it claims a job and marks it `processing`.
2. The executor extends `locked_until = now + lease_seconds` again when it actually starts.
3. On completion or error the executor releases the lease (`locked_until = now`).
4. The reaper only requeues a job whose lease expired more than `grace` seconds ago.

The claim query only selects jobs where `locked_until <= now`, so a validly leased job is invisible to it. Duplication occurs when a job becomes visible to the claim query while it should still be leased, for example when the lease value is written incorrectly (the epoch/1970 bug) or when the lease has genuinely expired because execution started far later than claim.

## Known issues under investigation

- **created_at overwrite.** `created_at` values on jobs or runs have been observed changing after creation (for example 15:07 to 15:11). Since `created_at` is the executor's correlation key, this must be found and stopped. Check every `db.edit` in the tick and executors for any that writes `created_at`.
- **Lease value integrity.** `lease_seconds` from the env var must be cast to int before `add_secs_to_timestamp`, or `locked_until` is written as epoch (1970), making the job permanently claimable. Confirmed and fixed in `claim_image_jobs`.
- **Intra-tick re-claim.** The drain loop calls `claim_image_jobs` up to `max_loops` times per tick. If a claim's `processing` write is not visible to the next loop's query, the same job could be claimed twice within one tick.
- **Duplicate cost.** Every duplicate claim results in a second full image generation, incurring OpenAI cost and consuming an async pool slot.

## Related notes

- [[story-creation-flow]]
- [[defer-image-pipeline-throughput-to-phase-2]]
- [[13. AI Text Generation - OpenAI]]
- [[14. AI Image Generation - OpenAI]]