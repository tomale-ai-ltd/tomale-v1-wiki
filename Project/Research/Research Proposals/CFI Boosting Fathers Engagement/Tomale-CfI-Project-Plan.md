# Tomale v2.0 — Project Plan
### Innovate UK CfI 2458 · Project period: Aug 2026 (M1) – Jul 2027 (M12)

**Pre-project activities shown from Jan 2026. Project start = Aug 2026.**

**Owner key**
| Code | Name | Role |
|---|---|---|
| PM | Kyle Burke | Project Manager / Founder |
| BE | Backend Engineer | AWS / ML engineer (to be recruited) |
| NRG | Neuro Rehab Group | Lead: Rachel Moir (SLT); Clare Barr (SLT) |
| IE | Dr Nicolas Cummins | Independent Evaluator (KCL) |
| EA | Stacey Kelsall | Educational Advisor |

**★ = billing milestone.** The starred task is the claim evidence that triggers the associated WP payment.

---

## WP0 — Project Initiation

| Task Name                                                                                                                 | Task ID | Owner | Dependencies | Start | End   |
| ------------------------------------------------------------------------------------------------------------------------- | ------- | ----- | ------------ | ----- | ----- |
| **WP0 — Project Initiation**                                                                                              | 0       | PM    | —            | 01/26 | 10/26 |
| **Fundraising and contract**                                                                                              | 0.1     | PM    | —            | 01/26 | 08/26 |
| CfI approval process — submit required docs for final suitability checks                                                  | 0.1.1   | PM    | —            | 01/26 | 07/26 |
| Set up overdraft facility for working capital (target: 60-day worst-case cashflow cover)                                  | 0.1.2   | PM    | 0.1.1        | 06/26 | 08/26 |
| **Key appointments**                                                                                                      | 0.2     | PM    | 0.1          | 08/26 | 09/26 |
| Issue consultancy and advisory agreements with NRG, Nick Cummins and Stacey Kelsall                                       | 0.2.1   | PM    | 0.1          | 08/26 | 08/26 |
| Recruit and onboard backend engineer (12-month FTC, PAYE)                                                                 | 0.2.2   | PM    | 0.1          | 08/26 | 09/26 |
| Issue subcontractor agreements including IP assignment terms compatible with the CfI head contract (Clauses 7.1.2 and 14) | 0.2.3   | PM    | 0.2.1        | 08/26 | 08/26 |
| Submit KCL due diligence request for Dr Cummins (6-week process — submit on project day 1)                                | 0.2.4   | PM    | 0.2.1        | 08/26 | 08/26 |
| **R&D process begins**                                                                                                    | 0.3     | PM    | 0.2          | 08/26 | 10/26 |
| Organise initial steering group meetings — agree ToR, schedule and cadence                                                | 0.3.1   | PM    | 0.2.1        | 08/26 | 08/26 |
| Begin co-design with SLTs and educational advisor — initial archetype topic and coaching-technique scoping                | 0.3.2   | PM    | 0.3.1        | 08/26 | 09/26 |
| ★ Produce PID and secure steering group sign-off (M1 billing milestone evidence)                                          | 0.3.3   | PM    | 0.3.1, 0.3.2 | 08/26 | 08/26 |
| Prepare and submit ethics application to independent research ethics committee                                            | 0.3.4   | PM    | 0.3.3        | 08/26 | 09/26 |
| Complete DPIA (Data Protection Impact Assessment)                                                                         | 0.3.5   | PM    | 0.3.3        | 08/26 | 09/26 |
| Initiate enhanced DBS checks for all staff and subcontractors working with children                                       | 0.3.6   | PM    | 0.2.1, 0.2.2 | 08/26 | 08/26 |
| Draft and adopt safeguarding policy                                                                                       | 0.3.7   | NRG   | 0.3.3        | 08/26 | 09/26 |
| Establish foreground IP register (Schedule C per CfI contract) and log initial entries                                    | 0.3.8   | PM    | 0.3.3        | 08/26 | 08/26 |
| Configure PM tooling — Linear, GitHub, shared decision log                                                                | 0.3.9   | PM    | 0.1          | 08/26 | 08/26 |
| M&E framework design — begins M1, completes M3 subject to KCL due diligence approval                                      | 0.3.10  | IE    | 0.2.4        | 08/26 | 10/26 |
| Design assessment criteria and outcome measures with SLTs and educational advisor (feeds WP2 and WP5 baselines)           | 0.3.11  | NRG   | 0.3.2        | 08/26 | 09/26 |



| **WP1 — Character-Consistent Illustration Pipeline**                                                                                                                                                                | 1     | BE  | 0.2.2               | 08/26 | 11/26 |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- | --- | ------------------- | ----- | ----- |
| **1.1 — Golden dataset and AWS environment setup**                                                                                                                                                                  | 1.1   | BE  | 0.2.2, 0.3.3        | 08/26 | 09/26 |
| Define evaluation criteria, scoring methodology and 80% combined pass/fail threshold (CLIP × 0.4 + human × 0.6)                                                                                                     | 1.1.1 | PM  | 0.3.3               | 08/26 | 08/26 |
| Compile golden dataset — story generation prompts, character JSON schemas, good and bad output examples covering all 3 artwork styles and single / two-character / three-character scenes                           | 1.1.2 | BE  | 1.1.1               | 08/26 | 09/26 |
| Upload reference data to S3 (eu-west-2 London) — prompt library, character JSON, training images (min. 50 reference images per style), validation set                                                               | 1.1.3 | BE  | 1.1.2               | 09/26 | 09/26 |
| Configure AWS environment — Bedrock API access, SageMaker IAM roles and permissions, S3 bucket structure, CloudWatch monitoring                                                                                     | 1.1.4 | BE  | 0.2.2               | 08/26 | 09/26 |
| **1.2 — Phase A: Bedrock model benchmarking**                                                                                                                                                                       | 1.2   | BE  | 1.1                 | 09/26 | 10/26 |
| Adapt existing DALL-E 3 prompts to Bedrock-compatible format for Stability AI models — preserve character attribute JSON, story context and artwork style descriptors                                               | 1.2.1 | BE  | 1.1.2, 1.1.4        | 09/26 | 09/26 |
| Run benchmark test set against Stable Image Core via Bedrock API — single, two and three-character scenes across all 3 artwork styles                                                                               | 1.2.2 | BE  | 1.2.1, 1.1.3        | 09/26 | 10/26 |
| Run benchmark test set against Stable Diffusion 3 Large via Bedrock API — same test scenarios as 1.2.2                                                                                                              | 1.2.3 | BE  | 1.2.1, 1.1.3        | 09/26 | 10/26 |
| Apply image-to-image conditioning — pass reference character image as starting point to each Bedrock model; assess consistency improvement vs prompt-only baseline                                                  | 1.2.4 | BE  | 1.2.2, 1.2.3        | 10/26 | 10/26 |
| Score all Phase A outputs — automated CLIP normalised score; blinded human review by PM (style accuracy, character consistency, age-appropriateness on 1–5 scale)                                                   | 1.2.5 | PM  | 1.2.2, 1.2.3, 1.2.4 | 10/26 | 10/26 |
| ★ Produce Phase A benchmarking report (M3 billing milestone evidence) — per-model combined scores, attribute bleed assessment, per-model unit-cost projection, Phase B recommendation                               | 1.2.6 | PM  | 1.2.5               | 10/26 | 10/26 |
| **1.3 — Phase B: SDXL fine-tuning and IP-Adapter**                                                                                                                                                                  | 1.3   | BE  | 1.2.6, 1.1          | 10/26 | 11/26 |
| Provision SageMaker asynchronous inference endpoint — SDXL on ml.g5.2xlarge, auto-scaling, scale-to-zero after 15 minutes inactivity                                                                                | 1.3.1 | BE  | 1.1.4               | 10/26 | 10/26 |
| Execute DreamBooth-LoRA training jobs on SageMaker — one per artwork style (3 styles); store adapter weights in S3; configure dynamic loading at inference time                                                     | 1.3.2 | BE  | 1.3.1, 1.1.2        | 10/26 | 11/26 |
| Implement Image Prompt Adapter (IP-Adapter) — reference image as additional conditioning input alongside text prompt to maintain character identity across pages and multi-character scenes                         | 1.3.3 | BE  | 1.3.1               | 10/26 | 11/26 |
| Evaluate SDXL + LoRA + IP-Adapter outputs against golden dataset — measure attribute bleed reduction in multi-character scenes; compare against DALL-E 3 baseline and Phase A results                               | 1.3.4 | BE  | 1.3.2, 1.3.3, 1.1.2 | 11/26 | 11/26 |
| Apply combined scoring (CLIP × 0.4 + human × 0.6) — validate Phase B pipeline against 80% acceptance threshold                                                                                                      | 1.3.5 | PM  | 1.3.4               | 11/26 | 11/26 |
| **1.4 — Integration, testing and PD-01 delivery**                                                                                                                                                                   | 1.4   | BE  | 1.3.5               | 11/26 | 11/26 |
| Integrate selected image generation approach into existing async job / executor pipeline (Xano image_jobs, image_worker_tick executors)                                                                             | 1.4.1 | BE  | 1.3.5, 1.2.6        | 11/26 | 11/26 |
| End-to-end story generation test — full story (10–24 images) via integrated pipeline including character reference conditioning                                                                                     | 1.4.2 | BE  | 1.4.1               | 11/26 | 11/26 |
| Configure CloudWatch monitoring for inference endpoint — latency, error rate, cold-start metrics                                                                                                                    | 1.4.3 | BE  | 1.4.1               | 11/26 | 11/26 |
| Confirm and document UK data residency (eu-west-2) — update data-handling register and DPIA if required                                                                                                             | 1.4.4 | PM  | 1.4.1               | 11/26 | 11/26 |
| ★ Produce PD-01 validated pipeline documentation (M4 billing milestone evidence) — architecture decision record, benchmark results summary, acceptance criteria met, cost-per-image comparison vs DALL-E 3 baseline | 1.4.5 | PM  | 1.4.2, 1.4.3, 1.4.4 | 11/26 | 11/26 |
| Update foreground IP register (Schedule C) with WP1 outputs                                                                                                                                                         | 1.4.6 | PM  | 1.4.5               | 11/26 | 11/26 |


|Task Name|Task ID|Owner|Dependencies|Start|End|
|---|---|---|---|---|---|
|**WP2 — Story Archetype Library**|2|NRG|0.3.2, 0.3.11|09/26|12/26|
|**2.1 — Topic research and archetype selection (Discover / Define)**|2.1|NRG|0.3.2, 0.3.11|09/26|10/26|
|SLT-led workshop — identify topics fathers most commonly avoid or struggle to discuss, drawing on NRG clinical caseload and relevant literature|2.1.1|NRG|0.3.2|09/26|09/26|
|Cross-reference topic list with EYFS PSED learning goals — identify which unaddressed topics most impede children's social and emotional development at ages 3–5|2.1.2|NRG|2.1.1, 0.3.11|09/26|10/26|
|Prioritise and agree the archetype topic set — steering group review and sign-off on the final topic list, scoped to the pilot age range and timescale|2.1.3|PM|2.1.1, 2.1.2|10/26|10/26|
|Document father-engagement barriers per topic — why each topic is challenging for fathers (emotional, cultural, uncertainty); output feeds WP3 coaching-technique design|2.1.4|NRG|2.1.3|10/26|10/26|
|**2.2 — Archetype narrative design (Develop)**|2.2|NRG|2.1.3|10/26|11/26|
|Design narrative structure template per archetype — beginning / middle / end framework, character roles, emotional arc, age-appropriate vocabulary and scene guidance|2.2.1|NRG|2.1.3, 2.1.4|10/26|11/26|
|Develop archetype-specific prompt schema — extend the existing data_models template and output-schema pattern; define JSON output structure and generation constraints per topic|2.2.2|NRG|2.2.1|10/26|11/26|
|Generate sample stories per archetype using new schemas — review for narrative coherence, PSED developmental alignment, child safety and content moderation compliance|2.2.3|BE|2.2.2|11/26|11/26|
|SLT fidelity review — NRG assesses each archetype for developmental validity, appropriateness of topic handling and safe resolution of the narrative|2.2.4|NRG|2.2.3|11/26|11/26|
|Educational advisor review — Stacey confirms stories are pitched at the 3–5 year range, vocabulary complexity is appropriate and content aligns with EYFS curriculum|2.2.5|EA|2.2.3|11/26|11/26|
|**2.3 — Platform encoding, testing and D-02 delivery (Deliver)**|2.3|BE|2.2.4, 2.2.5|11/26|12/26|
|Encode archetype schemas in the platform data_models framework — create versioned prompt templates and output schema definitions for each topic|2.3.1|BE|2.2.2, 2.2.4|11/26|12/26|
|Test constrained generation — validate that generated stories consistently preserve the intended archetype structure, narrative arc and topic framing|2.3.2|BE|2.3.1|12/26|12/26|
|NRG final sign-off — SLT approval of encoded archetype library; documented written sign-off per topic|2.3.3|NRG|2.3.2|12/26|12/26|
|★ Produce D-02 archetype library documentation (M5 billing milestone evidence) — signed archetype library, schema documentation, design rationale and father-barrier notes per topic|2.3.4|PM|2.3.3|12/26|12/26|
|Update foreground IP register (Schedule C) with WP2 outputs|2.3.5|PM|2.3.4|12/26|12/26|



| Task Name                                                                                                                                                                                                           | Task ID | Owner | Dependencies        | Start | End   |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ----- | ------------------- | ----- | ----- |
| **WP3 — Father-Coaching Chatbot Workflows**                                                                                                                                                                         | 3       | NRG   | 0.3.2, 0.3.7, 2.1.3 | 10/26 | 01/27 |
| **3.1 — Coaching technique co-design**                                                                                                                                                                              | 3.1     | NRG   | 0.3.2, 2.1.3        | 10/26 | 11/26 |
| NRG workshop — document the SLT-derived dialogic reading techniques to be coached: open questions, expansion, modelling and distancing; define the target behaviours fathers should exhibit during co-reading       | 3.1.1   | NRG   | 0.3.2               | 10/26 | 10/26 |
| Map coaching techniques to archetype topics — for each PD-02 archetype define the specific coaching prompts, expansions and cues appropriate to that topic and its emotional context                                | 3.1.2   | NRG   | 2.1.3, 2.1.4, 3.1.1 | 10/26 | 11/26 |
| Design the coaching conversation flow — structure the chatbot interaction: pre-story setup and intent-setting, per-page coaching prompts, handling of father responses, session close and reflection                | 3.1.3   | NRG   | 3.1.2               | 11/26 | 11/26 |
| Define safeguarding escalation triggers — identify language or content patterns requiring escalation; document the escalation pathway consistent with the safeguarding policy (0.3.7) and RCSLT clinical governance | 3.1.4   | NRG   | 0.3.7, 3.1.3        | 11/26 | 11/26 |
| **3.2 — System prompt and workflow architecture**                                                                                                                                                                   | 3.2     | BE    | 3.1.3, 2.2.2        | 11/26 | 12/26 |
| Design coaching layer system prompt architecture — how GPT-4o receives archetype context, story state, father input and coaching history to generate contextually appropriate coaching responses                    | 3.2.1   | BE    | 3.1.3, 2.2.2        | 11/26 | 11/26 |
| Define chatbot conversation state model — database objects for session progress, coaching prompts delivered, father response patterns and archetype adherence tracking                                              | 3.2.2   | BE    | 3.2.1               | 11/26 | 12/26 |
| Extend conversations API to support the coaching layer — new message types for coaching prompts, archetype-aware story page generation and bidirectional coaching feedback loop                                     | 3.2.3   | BE    | 3.2.1, 3.2.2        | 12/26 | 12/26 |
| Implement safety guardrail pipeline — extend the existing PASS / PARENTAL_OVERSIGHT / FAIL moderation to cover coaching context, safeguarding escalation triggers and age-appropriate content constraints           | 3.2.4   | BE    | 0.3.7, 3.1.4, 3.2.3 | 12/26 | 12/26 |
| **3.3 — Build, test and PD-03 delivery**                                                                                                                                                                            | 3.3     | BE    | 3.2, 2.3.1          | 12/26 | 01/27 |
| Build complete coaching chatbot workflows — implement all conversation flows, coaching prompts, archetype-aware generation and guardrails in the platform                                                           | 3.3.1   | BE    | 3.2.4, 2.3.1        | 12/26 | 01/27 |
| Internal safety testing — edge-case inputs, guardrail stress testing; verify safeguarding escalation triggers activate correctly and no unsafe content passes moderation                                            | 3.3.2   | BE    | 3.3.1               | 01/27 | 01/27 |
| SLT fidelity testing — NRG reviews chatbot coaching outputs for dialogic technique accuracy; confirm prompts correctly model open questions, expansion and child-talk elicitation across all archetypes             | 3.3.3   | NRG   | 3.3.1               | 01/27 | 01/27 |
| Iterate based on NRG feedback — refine coaching prompts, conversation flow and guardrail thresholds                                                                                                                 | 3.3.4   | BE    | 3.3.2, 3.3.3        | 01/27 | 01/27 |
| NRG sign-off — formal SLT approval of coaching dialogue protocols, technique accuracy and safety guardrails                                                                                                         | 3.3.5   | NRG   | 3.3.4               | 01/27 | 01/27 |
| ★ Produce PD-03 documentation (M6 billing milestone evidence) — coaching workflow specification, SLT-approved dialogue protocol library, safety testing results and sign-off record                                 | 3.3.6   | PM    | 3.3.5               | 01/27 | 01/27 |
| Update foreground IP register (Schedule C) with WP3 outputs                                                                                                                                                         | 3.3.7   | PM    | 3.3.6               | 01/27 | 01/27 |


| Task Name                                                                                                                                                                                               | Task ID | Owner | Dependencies        | Start | End   |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ----- | ------------------- | ----- | ----- |
| **WP4 — Integration, Analytics and Safety Gate**                                                                                                                                                        | 4       | BE    | 1.4.5, 2.3.4, 3.3.6 | 12/26 | 02/27 |
| **4.1 — Integration planning and environment setup**                                                                                                                                                    | 4.1     | PM    | 1.4.5, 2.3.4        | 12/26 | 01/27 |
| Review WP1, WP2 and WP3 handover outputs — assess integration scope, component interdependencies and risks; produce integration test plan                                                               | 4.1.1   | PM    | 1.4.5, 2.3.4        | 12/26 | 12/26 |
| Merge development environments into consolidated staging environment for end-to-end testing                                                                                                             | 4.1.2   | BE    | 4.1.1               | 12/26 | 01/27 |
| **4.2 — PD-04: Engagement analytics instrumentation**                                                                                                                                                   | 4.2     | BE    | 0.3.10, 3.2.2       | 12/26 | 01/27 |
| Agree engagement metrics with evaluator and NRG — session frequency, duration, initiation rate, completion rate, coaching prompt uptake and per-archetype engagement; align with IE's M&E framework     | 4.2.1   | PM    | 0.3.10              | 12/26 | 12/26 |
| Design analytics data model — event schema, session records and per-family longitudinal tracking structure                                                                                              | 4.2.2   | BE    | 4.2.1, 3.2.2        | 12/26 | 01/27 |
| Implement event instrumentation throughout co-authoring and coaching flow                                                                                                                               | 4.2.3   | BE    | 4.2.2               | 01/27 | 01/27 |
| Build evaluator data export — structured output feed aligned to Cummins's independent analysis requirements                                                                                             | 4.2.4   | BE    | 4.2.3               | 01/27 | 01/27 |
| Validate analytics data quality — verify event capture completeness, check for gaps and anomalies with evaluator                                                                                        | 4.2.5   | BE    | 4.2.4               | 01/27 | 01/27 |
| **4.3 — PD-01, PD-02 and PD-03 integration**                                                                                                                                                            | 4.3     | BE    | 4.1.2, 3.3.6        | 01/27 | 02/27 |
| Integrate PD-01 image pipeline into co-authoring flow — character-consistent illustrations generated per story page within the coaching workflow                                                        | 4.3.1   | BE    | 1.4.5, 4.1.2        | 01/27 | 01/27 |
| Integrate PD-02 archetype schemas into co-authoring flow — archetype selection, constrained generation and narrative structure feeding through the chatbot                                              | 4.3.2   | BE    | 2.3.4, 4.1.2        | 01/27 | 01/27 |
| Integrate PD-03 coaching chatbot with PD-01 and PD-02 — end-to-end flow: father selects archetype, chatbot coaches story co-creation, image pipeline generates consistent illustrations per page        | 4.3.3   | BE    | 3.3.6, 4.3.1, 4.3.2 | 01/27 | 02/27 |
| Integrate PD-04 analytics into complete flow — instrument full end-to-end user journey from archetype selection through story completion                                                                | 4.3.4   | BE    | 4.2.3, 4.3.3        | 02/27 | 02/27 |
| End-to-end integration test — full co-authoring and coaching session with all components; verify data integrity, moderation pipeline, error handling and performance                                    | 4.3.5   | BE    | 4.3.4               | 02/27 | 02/27 |
| **4.4 — Safety and fidelity gate + PD-05 delivery**                                                                                                                                                     | 4.4     | NRG   | 4.3.5               | 02/27 | 02/27 |
| Internal safety audit — adversarial input testing, guardrail stress test, moderation edge cases, safeguarding escalation trigger verification                                                           | 4.4.1   | BE    | 4.3.5               | 02/27 | 02/27 |
| NRG integrated platform review — SLTs review the full end-to-end experience; confirm coaching layer operates as designed when story generation and illustrations are combined in context                | 4.4.2   | NRG   | 4.3.5               | 02/27 | 02/27 |
| Educational advisor review — Stacey confirms the complete experience is age-appropriate for 3–5 year olds and suitable for father-led use                                                               | 4.4.3   | EA    | 4.3.5               | 02/27 | 02/27 |
| Iterate and resolve — address safety, fidelity or experience issues raised in 4.4.1–4.4.3                                                                                                               | 4.4.4   | BE    | 4.4.1, 4.4.2, 4.4.3 | 02/27 | 02/27 |
| NRG formal sign-off — documented SLT approval confirming the integrated platform is pilot-ready                                                                                                         | 4.4.5   | NRG   | 4.4.4               | 02/27 | 02/27 |
| ★ Produce PD-05 documentation (M7 billing milestone evidence) — integrated platform architecture, safety audit results, fidelity review outcomes, NRG sign-off record, acceptance criteria confirmation | 4.4.6   | PM    | 4.4.5               | 02/27 | 02/27 |
| Update foreground IP register (Schedule C) with WP4 outputs                                                                                                                                             | 4.4.7   | PM    | 4.4.6               | 02/27 | 02/27 |


| Task Name                                                                                                                                                       | Task ID | Owner | Dependencies | Start | End   |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ----- | ------------ | ----- | ----- |
| **WP5 — Pilot Delivery and Monitoring**                                                                                                                         | 5       | PM    | 4.4.6, 0.3.4 | 01/27 | 06/27 |
| **5.1 — Preparation**                                                                                                                                           | 5.1     | PM    | 0.3.4, 0.3.7 | 01/27 | 02/27 |
| Confirm ethics approval received — gate check before any participants are contacted; if approval has not been received by M6, escalate timeline with NRG and IE | 5.1.1   | PM    | 0.3.4        | 01/27 | 01/27 |
| Develop father onboarding materials — platform guide, study overview, coaching approach explainer, FAQ and session structure                                    | 5.1.2   | PM    | 4.4.6        | 01/27 | 02/27 |
| Develop participant information sheet and consent forms — compliant with ethics approval; reviewed by NRG                                                       | 5.1.3   | NRG   | 0.3.4, 0.3.7 | 01/27 | 01/27 |
| Activate recruitment channels — NRG referral network (Rachel), nursery and school partners; secondary channel via Tomale user funnel                            | 5.1.4   | NRG   | 5.1.1, 5.1.3 | 01/27 | 03/27 |
| Set up participant management and data tracking system — family records, consent status, session logs, engagement flags                                         | 5.1.5   | BE    | 4.2.2        | 01/27 | 02/27 |
| **5.2 — Recruitment, onboarding and baseline**                                                                                                                  | 5.2     | NRG   | 5.1, 4.4.6   | 02/27 | 03/27 |
| Screen and enrol eligible families — confirm eligibility criteria (child aged 3–5, father able to participate), initial approach via NRG referral network       | 5.2.1   | NRG   | 5.1.3, 5.1.4 | 02/27 | 03/27 |
| Obtain informed consent — signed consent forms for all 30 families                                                                                              | 5.2.2   | NRG   | 5.2.1        | 02/27 | 03/27 |
| Deliver individual father onboarding sessions — 30 sessions at 1 SLT day per father; introduce the study, the platform and the coaching approach                | 5.2.3   | NRG   | 5.1.2, 5.2.2 | 02/27 | 03/27 |
| Conduct baseline child language assessment — SLT-administered standardised language measure per child using criteria agreed in 0.3.11                           | 5.2.4   | NRG   | 5.2.2        | 02/27 | 03/27 |
| Conduct baseline father engagement assessment — record existing co-reading frequency, style and confidence level                                                | 5.2.5   | NRG   | 5.2.2        | 02/27 | 03/27 |
| Create family accounts and configure platform — profile setup, character creation and archetype selection per family                                            | 5.2.6   | BE    | 4.4.6, 5.2.2 | 03/27 | 03/27 |
| Compile and share baseline dataset with evaluator                                                                                                               | 5.2.7   | PM    | 5.2.4, 5.2.5 | 03/27 | 03/27 |
| ★ WP5.1 billing milestone (M8) — 30 signed consent forms; baseline dataset complete; ethics approval confirmed; all families onboarded with accounts configured | 5.2.8   | PM    | 5.2.6, 5.2.7 | 03/27 | 03/27 |
| **5.3 — Pilot delivery months 1–2**                                                                                                                             | 5.3     | PM    | 5.2.8, 4.4.6 | 03/27 | 05/27 |
| Families begin home platform use — co-authoring and coaching sessions at home, self-directed with support available                                             | 5.3.1   | PM    | 5.2.6, 4.4.6 | 03/27 | 05/27 |
| Deliver monthly SLT therapy check-ins months 1–2 — 30 individual 1-hour sessions per month; review engagement, coaching uptake and family wellbeing             | 5.3.2   | NRG   | 5.3.1        | 03/27 | 05/27 |
| Ongoing engagement monitoring — PM reviews analytics dashboard weekly; flags low-engagement families to NRG for follow-up                                       | 5.3.3   | PM    | 5.3.1        | 03/27 | 05/27 |
| Technical support and issue resolution — address platform bugs, usability issues or data anomalies reported during pilot                                        | 5.3.4   | BE    | 5.3.1        | 03/27 | 05/27 |
| Compile mid-point engagement dataset months 1–2 — structured export for evaluator                                                                               | 5.3.5   | PM    | 5.3.3        | 05/27 | 05/27 |
| ★ WP5.2 billing milestone (M10) — mid-point engagement dataset delivered; therapy check-in records months 1–2 for all 30 families                               | 5.3.6   | PM    | 5.3.2, 5.3.5 | 05/27 | 05/27 |
| **5.4 — Pilot delivery months 3–4 and endline**                                                                                                                 | 5.4     | PM    | 5.3.6        | 05/27 | 06/27 |
| Continue home platform use months 3–4                                                                                                                           | 5.4.1   | PM    | 5.3.6        | 05/27 | 06/27 |
| Deliver monthly SLT therapy check-ins months 3–4 — 30 individual 1-hour sessions per month                                                                      | 5.4.2   | NRG   | 5.3.6        | 05/27 | 06/27 |
| Engagement monitoring months 3–4                                                                                                                                | 5.4.3   | PM    | 5.4.1        | 05/27 | 06/27 |
| Conduct endline child language assessment — SLT-administered standardised measure per child using same protocol as baseline                                     | 5.4.4   | NRG   | 5.4.1        | 06/27 | 06/27 |
| Conduct endline father engagement assessment                                                                                                                    | 5.4.5   | NRG   | 5.4.1        | 06/27 | 06/27 |
| Lock endline dataset — compile all measurements; validate completeness and quality with evaluator                                                               | 5.4.6   | PM    | 5.4.4, 5.4.5 | 06/27 | 06/27 |
| Produce pilot delivery summary — participation rates, attrition, issues and resolutions, narrative delivery account                                             | 5.4.7   | PM    | 5.4.6        | 06/27 | 06/27 |
| ★ WP5.3 billing milestone (M11) — dataset locked; all 30 families completed; pilot delivery summary                                                             | 5.4.8   | PM    | 5.4.7        | 06/27 | 06/27 |

---


|Task Name|Task ID|Owner|Dependencies|Start|End|
|---|---|---|---|---|---|
|**WP6 — Independent Evaluation and Reporting**|6|IE|5.4.8, 0.3.10|03/27|07/27|
|**6.1 — Analysis preparation (during pilot)**|6.1|IE|5.2.8, 0.3.10|03/27|05/27|
|Finalise pre-specified analysis plan — document engagement and outcome analysis methodology before data is unblinded; register with ethics committee if required|6.1.1|IE|0.3.10, 5.2.8|03/27|03/27|
|Prepare analysis environment — configure statistical software and data pipeline from PD-04 analytics export|6.1.2|IE|4.2.4, 5.2.8|03/27|04/27|
|Mid-pilot data quality check — review WP5.2 mid-point dataset for completeness and anomalies; flag any collection issues to PM|6.1.3|IE|5.3.6|05/27|05/27|
|**6.2 — Independent analysis (post pilot completion)**|6.2|IE|5.4.8|06/27|07/27|
|Receive and validate locked endline dataset — confirm completeness, data quality and integrity before analysis begins|6.2.1|IE|5.4.8|06/27|06/27|
|Analyse engagement outcomes — quantitative analysis of all metrics (frequency, duration, initiation, completion, coaching prompt uptake) vs baseline and pre-defined success criteria|6.2.2|IE|6.2.1|06/27|07/27|
|Analyse child language outcomes — endline vs baseline comparison using SLT-administered standardised language measures; calculate effect size estimates|6.2.3|IE|6.2.1|06/27|07/27|
|Objective speech-based language analysis — apply speech-as-digital-biomarker methodology to available speech samples as a supplementary and novel outcome measure|6.2.4|IE|6.2.1|06/27|07/27|
|Assess PSED and school-readiness indicators — review SLT and educational advisor records for PSED evidence; Stacey provides EYFS framework interpretation|6.2.5|EA|6.2.1|06/27|07/27|
|Finalise independent analysis — IE completes all analysis independently; NRG does not participate in analysis decisions|6.2.6|IE|6.2.2, 6.2.3, 6.2.4, 6.2.5|07/27|07/27|
|**6.3 — Evaluation report and project deliverables**|6.3|IE|6.2.6|07/27|07/27|
|Draft evaluation report — methodology, engagement findings, child language and PSED signal, limitations and Phase 2 recommendations|6.3.1|IE|6.2.6|07/27|07/27|
|PM review of draft — verify factual accuracy against project delivery records; flag inconsistencies for IE to resolve|6.3.2|PM|6.3.1|07/27|07/27|
|Finalise evaluation report|6.3.3|IE|6.3.2|07/27|07/27|
|★ PD-06: Independent evaluation report (WP6 billing milestone, M12) — complete independent analysis of engagement and child language outcomes vs pre-defined criteria|6.3.4|IE|6.3.3|07/27|07/27|
|PD-07: Final project report — comprehensive summary of all WP outputs, evaluation findings and lessons learned; submitted to the Authority within 14 days of project end per contract Clause 13.1|6.3.5|PM|6.3.4|07/27|07/27|
|Update foreground IP register (Schedule C) with WP6 outputs|6.3.6|PM|6.3.5|07/27|07/27|


|Task Name|Task ID|Owner|Dependencies|Start|End|
|---|---|---|---|---|---|
|**WP7 — Commercial Feasibility and Phase 2 Planning**|7|PM|5.4.8, 6.3.1|06/27|07/27|
|**7.1 — Commercial feasibility analysis**|7.1|PM|5.4.8, 1.4.5|06/27|07/27|
|Validate unit economics — using actual PD-01 pipeline costs, calculate cost per image and per story on the new architecture; compare to DALL-E 3 baseline and target subscription price point|7.1.1|PM|1.4.5|06/27|06/27|
|Analyse pilot adoption indicators — review engagement rates, family feedback and SLT assessments for commercial viability signals; assess whether fathers want to continue using the product|7.1.2|PM|5.4.8, 6.2.2|06/27|07/27|
|Map routes to market — assess commercial viability of each channel: SLT services (private and NHS), early-years settings, direct-to-consumer subscription, B2B licensing to schools and nurseries|7.1.3|PM|7.1.2|07/27|07/27|
|Review IP position — confirm foreground IP register is complete; assess patentability of novel elements; document commercial exploitation strategy per contract Clause 15 and Clause 15.4|7.1.4|PM|1.4.6, 2.3.5, 3.3.7, 4.4.7, 6.3.6|07/27|07/27|
|**7.2 — Phase 2 planning**|7.2|PM|6.3.1, 7.1.2|06/27|07/27|
|Define Phase 2 scope and design — RCT, scaled deployment or phased roll-out; target cohort; channel; drawing on WP6 draft evaluation findings|7.2.1|PM|6.3.1|06/27|07/27|
|Develop Phase 2 funding strategy — identify potential funders (CfI Phase 2, Innovate UK, NHS procurement, local authority, private investment); assess feasibility and indicative timeline|7.2.2|PM|7.2.1|07/27|07/27|
|Draft Phase 2 implementation plan — objectives, budget range, team, partner requirements, success criteria and progression milestones|7.2.3|PM|7.2.1, 7.2.2|07/27|07/27|
|Develop exploitation plan — IP management strategy, sales and marketing channels, pricing model and partner development roadmap; satisfies contract Clause 15.4|7.2.4|PM|7.1.3, 7.1.4, 7.2.3|07/27|07/27|
|**7.3 — WP7 deliverables and project close**|7.3|PM|7.1, 7.2, 6.3.4|07/27|07/27|
|★ PD-08: Commercial feasibility report and Phase 2 plan (WP7 billing milestone, M12) — unit economics validation, route-to-market analysis, Phase 2 implementation plan|7.3.1|PM|7.1.3, 7.2.3|07/27|07/27|
|PD-09: Exploitation plan — IP management, commercial strategy, sales and marketing, Phase 2 funding pathway|7.3.2|PM|7.2.4|07/27|07/27|
|Final foreground IP register update (Schedule C) — confirm all WP outputs are logged and the register is complete|7.3.3|PM|7.3.1, 7.3.2, 6.3.6|07/27|07/27|
|Project close — final invoicing, contract obligations checklist, team and subcontractor offboarding|7.3.4|PM|6.3.5, 7.3.1, 7.3.2, 7.3.3|07/27|07/27|

---

## Project Deliverables Summary

| PD    | Title                                                          | WP  | Owner    | Target completion |
| ----- | -------------------------------------------------------------- | --- | -------- | ----------------- |
| PD-01 | Character-consistent illustration pipeline                     | WP1 | BE       | Nov 26 (M4)       |
| PD-02 | Story archetype library                                        | WP2 | NRG      | Dec 26 (M5)       |
| PD-03 | Father-coaching chatbot workflows                              | WP3 | NRG / BE | Jan 27 (M6)       |
| PD-04 | Engagement analytics instrumentation layer                     | WP4 | BE       | Feb 27 (M7)       |
| PD-05 | Integrated pilot-ready build (safety and fidelity gate passed) | WP4 | BE / NRG | Feb 27 (M7)       |
| PD-06 | Independent evaluation report                                  | WP6 | IE       | Jul 27 (M12)      |
| PD-07 | Final project report                                           | WP6 | PM       | Jul 27 (M12)      |
| PD-08 | Commercial feasibility report and Phase 2 plan                 | WP7 | PM       | Jul 27 (M12)      |
| PD-09 | Exploitation plan                                              | WP7 | PM       | Jul 27 (M12)      |

---

## Billing Milestones Summary

| #   | Month        | WP    | Milestone                      | Evidence                                                                                  | Est. payment |
| --- | ------------ | ----- | ------------------------------ | ----------------------------------------------------------------------------------------- | ------------ |
| 1   | M1 (Aug 26)  | WP0   | Project initiation complete    | PID; steering group ToR; ethics application submitted; DPIA draft; DBS initiated          | £22,000      |
| 2   | M3 (Oct 26)  | WP1a  | Bedrock benchmarking complete  | Benchmarking report: CLIP and human review scores, unit-cost projections                  | £25,000      |
| 3   | M4 (Nov 26)  | WP1b  | PD-01 validated                | PD-01 pipeline meeting ≥80% threshold; SDXL + LoRA + IP-Adapter; architecture document    | £32,000      |
| 4   | M5 (Dec 26)  | WP2   | PD-02 complete                 | PD-02 SLT-signed archetype library; schema-encoded; steering group sign-off               | £20,000      |
| 5   | M6 (Jan 27)  | WP3   | PD-03 complete                 | PD-03 coaching chatbot; SLT-approved dialogue protocols; safety testing results           | £25,000      |
| 6   | M7 (Feb 27)  | WP4   | PD-05 safety gate passed       | PD-04 analytics layer; PD-05 integrated build with NRG sign-off                           | £32,000      |
| 7   | M8 (Mar 27)  | WP5.1 | Cohort recruited and baselined | 30 signed consent forms; baseline dataset; ethics approval confirmed; accounts configured | £52,000      |
| 8   | M10 (May 27) | WP5.2 | Mid-pilot delivery complete    | Mid-point engagement dataset; therapy check-in records months 1–2 for all 30 families     | £32,000      |
| 9   | M11 (Jun 27) | WP5.3 | Pilot complete                 | Endline dataset locked; all 30 families completed; pilot delivery summary                 | £35,000      |
| 10  | M12 (Jul 27) | WP6   | PD-06 delivered                | Independent evaluation report; blinded analysis of outcomes vs pre-defined criteria       | £42,000      |
| 11  | M12 (Jul 27) | WP7   | PD-08 delivered                | Commercial feasibility report; Phase 2 plan; exploitation plan                            | £18,000      |
|     |              |       | **Total**                      |                                                                                           | **£335,000** |

_Note: billing amounts are indicative pending final finance form reconciliation. Amounts must match the finance section in the IFS portal exactly._