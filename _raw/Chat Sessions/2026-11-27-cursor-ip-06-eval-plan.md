---
date: 2026-11-27
source: cursor
branch: 002-eval-harness
feature: 002-eval-harness
---

# IP-06 plan fixes + PR (no implement)

## What changed
- Applied Kyle’s five plan/spec fixes on `002-eval-harness`: unified Vertex eu judge; planner_model on all pipelines; Xano page/cover prompt sources + FR-003a; judge schema rework; Vertex pricing sources; I1 closed.
- Re-ran analyze; push + open PR (CI green); no tasks/implement.

## Decisions
- Judge: `gemini-3.1-flash-lite` @ Vertex `eu` for every pipeline; `gpt-4o-mini` is baseline planner only.
- Gemini image: aspect_ratio 3:2, image_size 2K (1K for -1k); baseline 1536x1024, no quality.
- Baseline prompts from `ai_pipeline_executor_page_image.xs` / `ai_pipeline_executor_cover_image.xs`.
- Flash Image retirement: May 28, 2027 or later (Vertex model-versions).

## Open questions / blockers
- None for this PR.

## Next
- After merge: `/speckit.tasks` then implement when Kyle asks.
