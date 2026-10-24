# Tomale CfI — Cost Model & Budget (Q11 + Finances)

### Innovate UK CfI 2458 · Revised: full-time engineer, individual onboarding, cohort 30

### Competition ceiling: £200k–£500k inclusive of VAT

**Hard constraints:**

- Total ≤ **£500,000** (competition ceiling; Tomale not VAT-registered)
- No profit — all costs at fair market value
- ≥50% of total must be R&D (exploration, design, prototyping, field testing)
- **Tomale's spend must exceed the combined subcontractors** (main binding constraint)
- Paid monthly in arrears against milestones

---

## 1. Headline budget (~£335k, ~£165k headroom)

| #   | IFS category         | Cost line                                                                | Who         |            £ |
| --- | -------------------- | ------------------------------------------------------------------------ | ----------- | -----------: |
| 1   | Labour               | Founder / technical lead (Kyle Burke), 1.0 FTE × 12 months               | Tomale      |      105,500 |
| 2   | Labour               | Backend engineer (AWS/ML), 1.0 FTE × 12 months                           | Tomale      |       88,000 |
| 3   | Overheads            | 10% of direct labour (own calculation)                                   | Tomale      |       17,600 |
| 4   | Materials            | Software, cloud compute and AI inference                                 | Tomale      |       15,000 |
| 5   | Capital usage        | Nil — all infrastructure cloud-based                                     | —           |            0 |
| 6   | Subcontracting       | NRG — specialist SLT clinical subcontract                                | NRG         |       49,650 |
| 7   | Subcontracting       | Independent evaluator (Dr Cummins)                                       | KCL/Cummins |       35,000 |
| 8   | Travel & subsistence | Steering group, pilot oversight, dissemination                           | Tomale      |        5,000 |
| 9   | Other costs          | Participant costs, outreach, ethics/DBS, insurance, workspace, reporting | Tomale      |       18,000 |
|     |                      | **TOTAL**                                                                |             | **£339,500** |


---

## 2. Labour — Kyle Burke (£90,000)

| Component                                                            |            £ |
| -------------------------------------------------------------------- | -----------: |
| Base salary (£75k FTE — defensible senior SWE/AI lead rate, UK 2026) |       90,000 |
| Employer NI (~15% on earnings above £5k secondary threshold)         |       12,750 |
| Pension (~3% auto-enrolment)                                         |        2,700 |
| **Fully loaded, 1.0 FTE**                                            | **£105,450** |

R&D split: ~80% R&D (TD-01 through TD-05, field testing), ~20% PM and reporting.

---

## 3. Labour — Backend engineer (£88,000)

|Component|£|
|---|--:|
|Base salary (£75k FTE — AWS ML engineer, Bedrock/SageMaker/SDXL)|75,000|
|Employer NI|~10,500|
|Pension|~2,250|
|**Fully loaded, 1.0 FTE**|**~88,000**|

Justification for 1.0 FTE: TD-01 (Bedrock benchmarking, SDXL/LoRA/IP-Adapter pipeline) realistically requires 6–8 months of focused engineering work. TD-02 and TD-03 backend integration, TD-04 analytics instrumentation and the integrated pilot-ready build (TD-05) require the remaining 4–6 months.

100% R&D. Primary workstream: TD-01.

---

## 4. Overheads (£17,600 — 10% own calculation)

10% of directly employed labour (£176,000 × 10%). Justification: lean startup with no admin staff or premises lease. Covers management software subscriptions, bookkeeping and accounting, employer liability and professional indemnity insurance, and general office consumables. Own calculation preferred over the 20% flat rate (which would add £35,200 and is disproportionate for a two-person startup).

---

## 5. Materials — software, cloud and AI (£15,000)

|Item|£|
|---|--:|
|AWS: Bedrock API, SageMaker GPU training jobs, S3, CloudWatch|7,500|
|OpenAI API (LLM text generation, chatbot, moderation)|3,500|
|EAS Build (React Native builds and distribution)|500|
|Dev tooling: Cursor Pro, GitHub Actions CI/CD, monitoring|1,500|
|Analytics, instrumentation and observability|500|
|Inference scaling contingency|1,500|
|**Total**|**15,000**|

---

## 6. Capital usage (£0)

No capital equipment. All infrastructure cloud-based (pay-as-you-go). N/A on IFS form.

---

## 7. Subcontracting — NRG (£49,650)

Rates: Rachel Moir (Director/SLT) £650/day; Clare Barr (SLT) £120/hour (£500/8hr day). Cohort: 30 families. Onboarding: individual sessions (1 SLT day per father).

| Phase            | Activity                                                       | Who            | Volume       | Rate          |          £ |
| ---------------- | -------------------------------------------------------------- | -------------- | ------------ | ------------- | ---------: |
| M1–M2 Design     | Archetype + assessment criteria design                         | Rachel         | 10 days      | £650/d        |      6,500 |
| M1–M2 Design     | Co-design support                                              | Clare          | 5 days       | £500/d        |      2,500 |
| M6–M7 Onboarding | Workshop prep (bespoke materials, resources, outcome measures) | Rachel + Clare | 3d × 2       | mix           |      3,450 |
| M6–M7 Onboarding | Individual father onboarding sessions (30 × 1 SLT day each)    | Clare          | 30 days      | £500/d        |     15,000 |
| M6–M7 Onboarding | Write-up and documentation                                     | Rachel         | 2 days       | £650/d        |      1,300 |
| M7–M10 Delivery  | Monthly therapy check-ins (30 × 4 months × 1h)                 | Clare          | 120 hours    | £120/h        |     14,400 |
| M7–M10 Delivery  | Travel                                                         | —              | 120 sessions | ~£20          |      2,400 |
| M11–M12 Eval     | Outcome administration + evaluation report input               | Rachel + Clare | 4d + 3d      | mix           |      4,100 |
|                  |                                                                |                |              | **NRG total** | **49,650** |

---

## 8. Subcontracting — independent evaluator (£35,000)

Dr Nicolas Cummins, Senior Lecturer KCL (Biostatistics & Health Informatics). £650/day.

|Task|Days|£|
|---|---|--:|
|M&E design, outcome measures, analysis plan (M1–M2)|8|5,200|
|Mid-pilot oversight (M7–M8)|3|1,950|
|Independent analysis + evaluation report (M11–12)|22|14,300|
|Speech-based child-language outcome analysis|10|6,500|
|KCL contracting buffer|—|7,050|
|**Total**|**43 days**|**35,000**|

---

## 9. Travel & subsistence (£5,000)

|Item|£|
|---|--:|
|Steering group meetings ×4 in-person|1,000|
|Pilot oversight visits (Kyle periodic attendance)|1,500|
|Dissemination / conference|1,500|
|Miscellaneous|1,000|
|**Total**|**5,000**|

NRG session travel is within the NRG subcontract.

---

## 10. Other costs (£18,000)

| Item                                                                                |          £ |
| ----------------------------------------------------------------------------------- | ---------: |
| Participant costs — incentives + keepsake printed books (30 families, ~£200/family) |      6,000 |
| Outreach, recruitment, NRG network events                                           |      3,000 |
| Independent research ethics review (application fee)                                |      1,000 |
| Enhanced DBS checks                                                                 |        500 |
| DPIA and data protection compliance                                                 |      1,000 |
| Professional indemnity + public liability insurance (project uplift)                |      1,500 |
| Co-working hot-desk (12 months, ~£175/month)                                        |      2,100 |
| Reporting, dissemination and final publication                                      |      2,000 |
| Miscellaneous                                                                       |        900 |
| **Total**                                                                           | **18,000** |

**On premises:** no office lease. A co-working hot-desk (~£2,100) covers a professional working environment. For onboarding sessions, NRG's premises or per-event room hire (~£150/event × 6 sessions = £900, included in miscellaneous above) is appropriate.

---

## 11. TD/work-package cost mapping

| Technical deliverable              | Primary cost lines                                                     | Approx. % of budget |
| ---------------------------------- | ---------------------------------------------------------------------- | ------------------: |
| TD-01 Illustration pipeline        | Backend engineer (60% of role), Kyle (~30% time), AWS/materials (~50%) |                ~35% |
| TD-02 Story archetypes             | Kyle (~15% time), NRG design phase (Rachel)                            |                 ~9% |
| TD-03 Coaching chatbot             | Kyle (~25% time), NRG chatbot consultation, LLM API                    |                ~12% |
| TD-04 Engagement analytics         | Kyle (~10% time), tooling                                              |                 ~4% |
| TD-05 Pilot-ready build + SLT gate | Kyle (~10% time), NRG clinical sign-off                                |                 ~5% |
| Pilot delivery                     | NRG clinical, Cummins evaluation, participant costs                    |                ~26% |
| PM + governance                    | Kyle (~10% non-R&D), overheads, ethics, workspace, reporting           |                 ~9% |

---

## 12. Eligibility tests

**≥50% R&D:**

|R&D item|£|
|---|--:|
|Kyle R&D time (80% × £88k)|70,400|
|Backend engineer (100%)|88,000|
|Software / AI inference (100%)|15,000|
|NRG R&D (~78% of £68k)|53,000|
|Cummins (100%)|35,000|
|**R&D subtotal**|**~261,400**|

**R&D = £261k / £335k = 78%** ✓

**Majority by applicant:**

||£|
|---|--:|
|Tomale (labour + overheads + materials + T&S + other)|~231,600|
|Subcontractors (NRG + Cummins)|103,000|

**Tomale £232k > subcontractors £103k (69% Tomale)** ✓

---

## 13. IFS portal form — category totals

|IFS category|£|
|---|--:|
|Labour|176,000|
|Overheads|17,600|
|Materials|15,000|
|Capital usage|0|
|Subcontracting|103,000|
|Travel & subsistence|5,000|
|Other costs|18,000|
|**Total**|**334,600**|

---

## 14. Confirmations needed

1. Engineer engagement type: employed/PAYE (Labour) vs contractor/freelance (Subcontracting)?
2. NRG and Cummins: are quoted rates ex-VAT or inclusive? If ex-VAT and suppliers are VAT-registered, gross up by 20%.
3. Your actual salary/FTE basis (£75k FTE confirmed?).
4. Cummins contracting route: personal consultancy vs KCL institutional contract.
5. Ethics review fee: confirm independent REC application fee estimate.
6. Confirm cohort is 30 with individual onboarding (back on the table given budget headroom).