---
type: entity
entity-type: tool
name: Postman
aliases: []
tags:
  - llm-wiki/entity
  - llm-wiki/entity/tool
source-count: 34
date-updated: 2026-10-24
cssclasses: []
---


# Postman

## Facts

- Postman collection maintenance is synchronized with Xano via OpenAPI import/merge.
- Fixed a Postman harness bug that had invalidated two earlier tests.
- A bug in Postman was fixed that had invalidated earlier tests.
- Fixed the Postman pre-request script and re-ran the two Stripe tests.
- Postman testing suite was set up to test API endpoints.
- Postman testing suite setup completed.
- Flow test scripts authored in Postman.
- A Postman testing suite was set up to validate API endpoints.
- Postman was used to set up metadata API observability.
- Used to build out assertions and run flow tests.
- Built a repeatable flow-test harness for story generation using Postman.
- A repeatable flow-test harness for story generation was built using Postman.
- Postman is used for building a repeatable flow-test harness for story generation.
- Used for the order-fulfilment flow-test.
- Used for testing the order-fulfilment flow and story creation.
- Used for automating the order-fulfilment flow-test in the project.
- Used for testing the order-fulfilment flow.
- Postman is used for testing the order-fulfilment flow.
- Postman is used to send a signed webhook for simulating Stripe payments.
- Used for testing the API endpoints and managing requests related to the project.
- Used for testing the API with a collection of tests for story fixes and order fulfillment.
- Postman is utilized for testing API endpoints and validating order fulfilment processes.
- Postman is utilized for testing API endpoints and managing requests.
- Postman is referenced in the context of polling for order submission.
- The batch update includes the Postman OpenAPI re-sync.
- Postman was used for testing API endpoints and encountered a token expiration issue.
- Postman 1B encountered a 'token expired' issue on the first run.
- Postman 1B had a 'token expired' issue on the first run.
- Postman tests were conducted to validate the cancel and refund functionalities.
- Postman was used to add cancel/refund tests.
- Used for testing cancel and refund processes.
- Postman covers the testing of the `auth/refresh` endpoint.
- Legacy Postman app auto-login script was deleted.
- Login tokens are set run-scoped in Postman.
- Postman was used for testing the parental-approval order gate.
- Postman was used for testing the parental-approval order gate and other functionalities.
- Legacy Postman app auto-login script was deleted and run-scoped token was set.
- Postman negative test was added for parental-approval order gate.
- Postman token handling was a focus area in the session.
- Postman is used for testing the API endpoints with a total of 86 tests.
- The Postman tests suite will not run in CI until it is split into a fast, safe subset.
- A negative Postman test covers the scenario of blocking orders awaiting parental approval.
- Postman is used for regression testing in the Tomale project.

## Connections

- [[flow-test-scripts]] *(related-to)*
- [[api-security-model]] *(uses)*
- [[metadata-api-observability]] *(uses)*
- [[tomale-rn-v1]] *(uses)*
- [[story-generation]] *(uses)*
- [[order-fulfilment-test-design]] *(uses)*
- [[order-fulfilment-flow-test]] *(uses)*
- [[manual-gates-replacement]] *(extends)*
- [[stripe]] *(uses)*
- [[order-fulfilment-delay]] *(related-to)*
- [[documentation-refresh]] *(part-of)*
- [[refund-process]] *(uses)*
- [[401-invalid-refresh-token-response]] *(uses)*
- [[xano]] *(uses)*
- [[newman]] *(contrasts-with)*
- [[tomale-rn-v1]] *(related-to)*
- [[tomale-v1]] *(uses)*
- [[xano]] *(uses)*
- [[tomale-rn-v1]] *(uses)*

## Sources

- [[Project/Decisions/adopt-openapi-import-for-postman-collection-sync.md]]
- [[_raw/Chat Sessions/_archive/2026-07-15-001.md]]
- [[Sessions/2026-07-15-001.md]]
- [[_raw/Chat Sessions/_archive/2026-07-16-001.md]]
- [[Sessions/2026-07-16-001.md]]
- [[_raw/Chat Sessions/_archive/2026-08-03-001.md]]
- [[Sessions/2026-08-03-001.md]]
- [[_raw/Chat Sessions/Untitled.md]]
- [[_raw/Chat Sessions/_archive/2026-09-14-001.md]]
- [[Sessions/2026-09-14-001.md]]
- [[_raw/Chat Sessions/_archive/2026-10-12-001.md]]
- [[_raw/Chat Sessions/_archive/2026-10-09-001.md]]
- [[Sessions/2026-10-12-001.md]]
- [[Sessions/2026-10-09-001.md]]
- [[Project/Decisions/simulate-stripe-payment-with-signed-postman-webhook.md]]
- [[_raw/Chat Sessions/_archive/2026-10-13-001.md]]
- [[Sessions/2026-10-13-001.md]]
- [[_raw/Chat Sessions/_archive/2026-10-14-001.md]]
- [[Sessions/2026-10-14-001.md]]
- [[Project/Decisions/delay-hpbc-submission-with-30-minute-cancellation-window.md]]
- [[Project/Decisions/defer-documentation-refresh-until-after-phase-1-signoff.md]]
- [[_raw/Chat Sessions/_archive/2026-10-21-001.md]]
- [[_raw/Chat Sessions/_archive/2026-10-15-001.md]]
- [[Sessions/2026-10-15-001.md]]
- [[Sessions/2026-10-21-001.md]]
- [[Project/Decisions/return-401-invalid-refresh-token-from-auth-refresh.md]]
- [[_raw/Chat Sessions/_archive/2026-10-23-001.md]]
- [[_raw/Chat Sessions/_archive/2026-10-22-001.md]]
- [[Sessions/2026-10-23-001.md]]
- [[Sessions/2026-10-22-001.md]]
- [[Project/Plan/6-api-security-model.md]]
- [[Project/Decisions/defer-postman-suite-ci-until-suite-split.md]]
- [[Project/Decisions/block-ordering-of-stories-awaiting-parental-approval.md]]
- [[Project/Plan/operating-model.md]]
