---
type: entity
entity-type: project
name: Tomale
aliases: []
tags:
  - llm-wiki/entity
  - llm-wiki/entity/project
source-count: 26
date-updated: 2026-10-24
cssclasses: []
---


# Tomale

## Facts

- The project that the mobile app is built for, encompassing story creation, e-reader, characters, and store flows.
- GPT-4o sits at the core of the Tomale content pipeline.
- The immersive e-reader experience aligns with Tomale's mission.
- Tomale allows children to create AI-generated stories.
- This PRD defines a parental oversight system that locks sensitive content until a parent explicitly approves it.
- The project will follow a modified version of Semantic Versioning (SemVer) to align version increments with Expo's OTA vs app store release distinction.
- The decision to adopt ReBAC is part of the Tomale project.
- This document represents the full backend schema for the Tomale platform, generated from the Xano Metadata API.
- The document represents the full backend schema for the Tomale platform.
- This document represents the full backend schema for the Tomale platform.
- Current milestone is Phase 1 — Security & Data Integrity.
- Focus on API security model maintenance and integration decisions.
- The project is implementing a custom URL scheme for Stripe Checkout redirects.
- The session is part of the Tomale project, specifically the tomale-rn-v1 phase.
- The project involves the development of a user profile model and API endpoints for user authentication.
- The project involves using an HTTPS link for magic-link emails that directs users to the Tomale app.
- The project involves separating the verify-email deeplink from the magic-link completion path.
- An existing personalized children's-story platform being adapted for the project.
- Tomale SEND is an adapted version of Tomale focused on engaging fathers of EYFS children with additional speech & language needs.
- The project has a total budget of £250,000, with a target budget of £235,000.
- The project has a total budget of £250,000, which is VAT-inclusive.
- The project has a total budget of £250,000, with a target of £235,000.
- The project has a total budget of £250,000, with specific constraints on R&D spending and subcontractor costs.
- The total budget for Tomale is approximately £335k with a headroom of £165k.
- The project has a total budget of approximately £335k with a ceiling of £500k.
- The total budget for Tomale is approximately £335,000, with a headroom of £165,000.
- The total budget for Tomale is approximately £335k, with a headroom of ~£165k.
- The project has a total budget of approximately £335,000 with a headroom of £165,000.
- Tomale's spend must exceed the combined subcontractors.
- Tomale is not VAT-registered.
- The total budget for Tomale is approximately £335k with a headroom of ~£165k.
- The project has a total budget of approximately £335k with a headroom of £165k.
- The project has a budget ceiling of £500,000 and requires at least 50% of total costs to be allocated to R&D.
- The project has a total budget of approximately £335,000 with a ceiling of £500,000.
- The total budget for Tomale is approximately £335k, with a ceiling of £500k.
- The project has a total budget of approximately £335,000 with a hard ceiling of £500,000.
- The total budget for the project is approximately £335k, with a ceiling of £500k.
- The project involves user profiles work, including a two-stage name validation system and avatar design approach.
- The project involves user_profiles work, including a two-stage name validation system and avatar design approach.
- The project involves user_profiles work, including a two-stage name validation system and avatar design.
- The project involves user_profiles work and content moderation systems.
- The project is in phase-1 focusing on user alerts and phonics.
- The project is currently in phase 1 focusing on user alerts and API audit.
- The project involves an order and fulfilment flow for store orders.
- Money is stored as an integer, `amount_minor`, paired with `currency`, replacing the old float `price` field on `transactions`.
- The decision is part of the Tomale project, specifically the tomale-rn-v1 version.
- The project is currently in Phase 1, focusing on resolving image pipeline duplication issues.
- The project involves an image generation pipeline and related bug fixes.
- The documentation refresh is part of the Tomale RN V1 project.
- The documentation refresh is part of the Tomale project.
- Phase 1 signed off on 2026-10-23, focusing on Security & Data Integrity.
- Phase 1 signed off on 2026-10-23, focusing on security and data integrity.
- Current milestone is Phase 1 close-out.
- The project knowledge is spread across the Obsidian vault, the Cursor repo, and copies in the Claude Project.
- The decision is part of the Phase 1 sweep applied to various endpoints.
- The project aims to improve knowledge management across various repositories.
- The project aims to organize knowledge across the Obsidian vault, Cursor repo, and Claude Project.
- The project involves a knowledge architecture plan that includes various systems and sources.
- The project knowledge is spread across various tools including the Obsidian vault, Cursor repo, and Xano.

## Connections

- [[react-native]] *(applies-to)*
- [[expo]] *(applies-to)*
- [[immersive-e-reader-experience]] *(extends)*
- [[parental-oversight-system]] *(extends)*
- [[modified-semver-versioning]] *(uses)*
- [[expo]] *(related-to)*
- [[xano-metadata-api]] *(uses)*
- [[cursor]] *(uses)*
- [[api-security-model]] *(applies-to)*
- [[stripe]] *(uses)*
- [[xano]] *(uses)*
- [[squarespace]] *(uses)*
- [[resend]] *(uses)*
- [[email-verification-deeplink]] *(uses)*
- [[magic-link-completion-path]] *(contrasts-with)*
- [[kyle]] *(created-by)*
- [[nrg]] *(part-of)*
- [[kcl]] *(part-of)*
- [[rd-budgeting]] *(applies-to)*
- [[budget-constraints]] *(influences)*
- [[rd]] *(applies-to)*
- [[budget-constraints]] *(related-to)*
- [[cost-model]] *(part-of)*
- [[rd-allocation]] *(applies-to)*
- [[nrg]] *(uses)*
- [[kyle-burke]] *(created-by)*
- [[nrg]] *(related-to)*
- [[dr-nicolas-cummins]] *(related-to)*
- [[eligibility-tests]] *(applies-to)*
- [[rd-requirements]] *(applies-to)*
- [[userprofiles]] *(part-of)*
- [[content-moderation-system]] *(applies-to)*
- [[avatar-design-approach]] *(applies-to)*
- [[content-moderation-system]] *(uses)*
- [[avatar-design-approach]] *(uses)*
- [[useralerts]] *(part-of)*
- [[phonics]] *(part-of)*
- [[image-generation-pipeline]] *(part-of)*
- [[sentry]] *(uses)*
- [[papermill]] *(uses)*
- [[hpbc]] *(uses)*
- [[cursor]] *(part-of)*
- [[phase-1]] *(part-of)*
- [[knowledge-architecture]] *(applies-to)*
- [[obsidian]] *(part-of)*
- [[claude-project]] *(uses)*
- [[explicit-allowlists]] *(extends)*
- [[obsidian]] *(uses)*
- [[knowledge-architecture]] *(part-of)*
- [[dalle-3]] *(uses)*
- [[gpt-4o]] *(part-of)*
- [[rebac]] *(part-of)*
- [[obsidian]] *(part-of)*
- [[custom-url-scheme]] *(applies-to)*
- [[tomaleai-limited]] *(related-to)*
- [[tomale-v20]] *(extends)*
- [[kyle]] *(part-of)*
- [[kyle]] *(created-by)*
- [[kyle-burke]] *(created-by)*
- [[nrg]] *(related-to)*
- [[kyle-burke]] *(part-of)*
- [[nrg]] *(created-by)*
- [[dr-nicolas-cummins]] *(related-to)*
- [[content-moderation-system]] *(applies-to)*
- [[avatar-design-approach]] *(applies-to)*
- [[hpbc-aka-pureprint]] *(related-to)*
- [[papermill]] *(part-of)*
- [[stripe]] *(part-of)*
- [[claude-project]] *(related-to)*

## Sources

- [[Project/Stack/2. Frontend - React.md]]
- [[Project/Stack/13. AI Text Generation - OpenAI.md]]
- [[Project/Plan/Feature PRDs/PRD-E-Reader.md]]
- [[Project/Plan/Feature PRDs/PRD-Parental-Oversight-Content-Approval.md]]
- [[Project/Decisions/adopt-modified-semver-versioning.md]]
- [[Project/Decisions/adopt-rebac-auth-model.md]]
- [[Project/Cursor/data-model.md]]
- [[Sessions/2026-05-07-003.md]]
- [[Project/Decisions/use-custom-url-scheme-for-stripe-checkout-redirect-v1.md]]
- [[_raw/Chat Sessions/_archive/2026-05-11-001.md]]
- [[Project/Decisions/use-https-web-intermediary-for-magic-link-redirect.md]]
- [[Project/Decisions/separate-verify-email-deeplink-from-magic-link-path.md]]
- [[Project/Research/Research Proposals/CFI Boosting Fathers Engagement/Tomale-CfI-Fathers-Engagement-Draft-v1.md]]
- [[Project/Research/Research Proposals/CFI Boosting Fathers Engagement/Tomale-CfI-Cost-Model.md]]
- [[_raw/Chat Sessions/2026-06-29-001.md]]
- [[_raw/Chat Sessions/_archive/2026-06-29-001.md]]
- [[_raw/Chat Sessions/_archive/2026-07-02-001.md]]
- [[Project/Architecture/order-fulfilment-flow.md]]
- [[Project/Decisions/store-money-as-integer-minor-units.md]]
- [[Project/Decisions/record-transactions-drop-checkout-session-object.md]]
- [[_raw/Chat Sessions/_archive/2026-08-03-001.md]]
- [[Project/Plan/documentation-refresh-backlog.md]]
- [[_raw/Chat Sessions/_archive/2026-10-23-001.md]]
- [[_raw/Chat Sessions/_archive/2026-10-22-001.md]]
- [[Project/Plan/knowledge-architecture.md]]
- [[Project/Decisions/replace-dblink-inputs-with-explicit-allowlists.md]]
