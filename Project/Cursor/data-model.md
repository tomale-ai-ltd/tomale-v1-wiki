---
type: foundation
title: data-model
project: tomale-rn-v1
status: current
date: 2026-04-14
---

___
# Data Model

## Overview

This document represents the full backend schema for the Tomale platform, generated from the Xano Metadata API and transformed into a structured, LLM-friendly format.

It is designed to:
- Provide a clear, human-readable representation of all tables and fields
- Enable effective reasoning by AI tools (e.g. Cursor)
- Support backend development, debugging, and API design

---

## Key Conventions

### 1. Ownership Model
- `users_id` (to be migrated to `owner_user_id`) represents ownership
- All user-owned data should be scoped by user in queries

### 2. Naming
- Tables and fields should follow `snake_case`
- `_id` suffix indicates foreign key relationships

### 3. Relationships
- `belongs_to` relationships are inferred from `_id` fields
- Join tables represent many-to-many relationships

### 4. System vs User Data
Tables are broadly categorised as:
- **User Data** → directly tied to user activity (stories, characters, orders)
- **System / Reference Data** → static or configuration (themes, phonics, products)
- **Pipeline / Jobs** → async processing (image_jobs, pdf_jobs, executor_runs)

---

## Domain Groupings

### 🧠 Core Content (Stories & Characters)
- instant_stories
- instant_story_pages
- instant_story_characters
- characters
- conversations

### Content Configuration
- themes
- artwork_style
- data_models

### AI & Processing Pipeline
- image_jobs
- pdf_jobs
- executor_runs
- token_usage

### Commerce & Orders
- store_orders
- store_order_updates
- products
- shipping_options

### Billing & Subscriptions
- subscriptions
- transactions
- transaction_webhook_events

### Users & Accounts
- users
- user_sessions
- user_logs
- user_activities
- user_child_profiles
- user_alerts

### Moderation & Safety
- moderation_flags

### Phonics & Education System
- phonics_scheme
- phonics_scheme_phase
- phonics_phase_stage
- phonics_grapheme
- phonics_exceptions
- phonics_stage_grapheme
- phonics_stage_exceptions

### Locale & Misc
- locale_data
- activities
- fact
- support_requests

---

## How to Use This Document

When working with this schema:

1. **Start with domain grouping**
   - Identify which part of the system you're working in

2. **Find the primary table**
   - e.g. `instant_stories`

3. **Follow relationships**
   - Use `belongs_to` to trace dependencies

4. **Check indexes**
   - Important for performance-critical queries

5. **Respect ownership rules**
   - Always filter by user where applicable

---


## Table: activities
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| name | text | no | no |
| description | text | no | no |
| value | int | no | no |
| Completed | bool | no | no |
| open_date | date | no | yes |
| expiry_date | date | no | yes |
| created_at | timestamp | no | no |
| last_modified_at | timestamp | no | yes |

Indexes:
- primary (id)
- btree (created_at)

---

## Table: artwork_style
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| name | text | no | no |
| description | text | no | no |
| image_prompt_positive | text | no | no |
| image_prompt_negative | text | no | no |
| status | enum(Active, Inactive) | no | no |
| access_tier | text | no | no |
| plan_level | int | no | no |
| is_new | bool | no | no |
| story_style_count | int | no | no |
| sample_image | image | no | yes |
| created_at | timestamp | no | no |
| last_modified_at | timestamp | no | yes |

Indexes:
- primary (id)
- btree (created_at)

---

## Table: characters
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| name | text | no | no |
| physical_description | text | no | no |
| primary_attributes | object | no | no |
| face_attributes | object | no | no |
| eyes_attributes | object | no | no |
| hair_attributes | object | no | no |
| clothing_attributes | object | no | no |
| status | enum(active, archived) | no | no |
| is_deleted | bool | no | no |
| cover_image | image | no | yes |
| instant_stories_id | int | no | no |
| data_models_id | int | no | no |
| users_id | int | no | no |
| created_at | timestamp | no | no |
| last_modified_at | timestamp | no | yes |
| deleted_at | timestamp | no | yes |

Relationships:
- belongs_to → instant_stories
- belongs_to → data_models
- belongs_to → users

Indexes:
- primary (id)
- btree (created_at)

---

## Table: conversations
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| chat_messages | object | no | no |
| conversation_type | enum(story, character) | no | no |
| status | enum(active, complete, abandoned, failed) | no | no |
| users_id | int | no | no |
| instant_stories_id | int | no | no |
| characters_id | int | no | no |
| created_at | timestamp | no | no |
| last_modified_at | timestamp | no | yes |
| is_deleted | bool | no | no |
| deleted_at | timestamp | no | yes |

Relationships:
- belongs_to → users
- belongs_to → instant_stories
- belongs_to → characters

Indexes:
- primary (id)
- btree (created_at)

---

## Table: data_models
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| slug | text | no | no |
| name | text | no | no |
| type | enum(story-text, character-image, theme, artwork-style, story-page-image, story-cover-image, moderation-text, moderation-image) | no | no |
| version | text | no | no |
| is_default | bool | no | no |
| status | enum(active, draft, deprecated) | no | no |
| output_schema | json | no | no |
| prompt_template | text | no | no |
| model_settings | json | no | no |
| created_at | timestamp | no | no |
| last_modified_at | timestamp | no | yes |

Indexes:
- primary (id)
- btree (created_at)

---

## Table: executor_runs
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| executor_name | text | no | no |
| job_type | enum(cover-image, page-image, character-image, cover-pdf, inner-pdf) | no | no |
| status | enum(success, error, queued) | no | no |
| image_jobs_id | int | no | no |
| pdf_jobs_id | int | no | no |
| async_job_id | uuid | no | yes |
| api_request | json | no | no |
| api_response | json | no | no |
| executor_result | json | no | no |
| created_at | timestamp | no | no |
| started_at | timestamp | no | yes |
| completed_at | timestamp | no | yes |

Relationships:
- belongs_to → image_jobs
- belongs_to → pdf_jobs
- belongs_to → async_job

Indexes:
- primary (id)
- btree (created_at)

---

## Table: fact
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| Fact | text | no | no |
| created_at | timestamp | no | no |

Indexes:
- primary (id)
- btree (created_at)

---

## Table: image_jobs
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| job_type | enum(character-image, page-image, cover-image) | no | no |
| status | enum(queued, processing, complete, error_retry, error_terminal) | no | no |
| instant_stories_id | int | no | yes |
| instant_story_pages_id | int | no | yes |
| characters_id | int | no | yes |
| priority | int | no | no |
| attempt | int | no | no |
| max_attempts | int | no | no |
| created_at | timestamp | no | no |
| last_modified_at | timestamp | no | yes |
| locked_until | timestamp | no | yes |
| retry_at | timestamp | no | yes |

Relationships:
- belongs_to → instant_stories
- belongs_to → instant_story_pages
- belongs_to → characters

Indexes:
- primary (id)
- btree (created_at)

---

## Table: instant_stories
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| title | text | no | no |
| subtitle | text | no | no |
| user_prompt | text | no | no |
| synopsis | text | no | no |
| theme_id | int | no | no |
| artwork_style_id | int | no | yes |
| cover_image | image | no | yes |
| story_pdf | attachment | no | yes |
| users_id | int | no | no |
| data_models_id | int | no | no |
| status | enum(In Queue, Preparing, Done, Blocked, Draft) | no | no |
| status_moderation | enum(Pass, Fail, Parental Approval, Pending) | no | no |
| is_public | bool | no | no |
| is_deleted | bool | no | no |
| total_pages | int | no | no |
| images_remaining | int | no | no |
| Views | int | no | no |
| blocked_reason | text | no | no |
| parental_approval_required | bool | no | no |
| parent_approved | bool | no | no |
| created_at | timestamp | no | no |
| last_modified_at | timestamp | no | yes |
| completed_at | timestamp | no | yes |
| deleted_at | timestamp | no | yes |

Relationships:
- belongs_to → theme
- belongs_to → artwork_style
- belongs_to → users
- belongs_to → data_models

Indexes:
- primary (id)
- btree (created_at)

---

## Table: instant_story_pages
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| page_number | int | no | no |
| text | text | no | no |
| instant_stories_id | int | no | yes |
| created_at | timestamp | no | no |
| last_modified_at | timestamp | no | yes |
| image | image | no | yes |

Relationships:
- belongs_to → instant_stories

Indexes:
- primary (id)
- btree (created_at)

---

## Table: instant_story_characters
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| instant_stories_id | int | no | no |
| characters_id | int | no | no |
| created_at | timestamp | no | no |

Relationships:
- belongs_to → instant_stories
- belongs_to → characters

Indexes:
- primary (id)
- btree (created_at)

---

## Table: locale_data
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| Name | text | no | no |
| UNTERM_English_Short | text | no | no |
| official_name_en | text | no | no |
| ISO4217-currency_country_name | text | no | no |
| Dial_Code | text | no | no |
| ISO3166-1-Alpha-3 | text | no | no |
| ISO3166-1-numeric | int | no | no |
| ISO3166-1-Alpha-2 | text | no | no |
| ISO4217-currency_name | text | no | no |
| ISO4217-currency_alphabetic_code | text | no | no |
| ISO4217-currency_numeric_code | int | no | no |
| ISO4217-currency_minor_unit | int | no | no |
| Capital | text | no | no |
| Sub_region_Name | text | no | no |
| Region_Name | text | no | no |
| Continent | text | no | no |
| TLD | text | no | no |
| Geoname_ID | int | no | no |

Indexes:
- primary (id)

---

## Table: moderation_flags
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| created_at | timestamp | no | no |
| users_id | int | no | no |
| instant_stories_id | int | no | no |
| type | enum(text, image) | no | no |
| categories_triggered | enum(violence_non_graphic, "violence_graphic, bullying, hate_or_discrimination, sexual_content, child_safety_csam, self_harm, drugs, illegal_activity, scary_disturbing, sensitive_grief_loss, abuse_or_exploitation, copyright_explicit, copyright_derivative_similarity) | no | no |
| user_prompt | json | no | no |

Relationships:
- belongs_to → users
- belongs_to → instant_stories

Indexes:
- primary (id)
- btree (created_at)

---

## Table: pdf_jobs
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| job_type | enum(cover-pdf, inner-pdf) | no | no |
| status | enum(queued, processing, complete, error_retry, error_terminal) | no | no |
| store_orders_id | int | no | yes |
| priority | int | no | no |
| attempt | int | no | no |
| max_attempts | int | no | no |
| created_at | timestamp | no | no |
| last_modified_at | timestamp | no | yes |
| locked_until | timestamp | no | yes |
| retry_at | timestamp | no | yes |

Relationships:
- belongs_to → store_orders

Indexes:
- primary (id)
- btree (created_at)

---

## Table: phonics_exceptions
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| word | text | no | no |
| ipa | text | no | no |
| notes | text | no | no |
| active | bool | no | no |
| exception_type | enum(tricky word, common exception word) | no | no |
| created_at | timestamp | no | no |

Indexes:
- primary (id)
- btree (created_at)

---

## Table: phonics_grapheme
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| grapheme | text | no | no |
| ipa | text | no | no |
| example_words | text | no | no |
| type | enum(grapheme, digraph, trigraph, split digraph, tetragraph) | no | no |
| active | bool | no | no |

Indexes:
- primary (id)

---

## Table: phonics_phase_stage
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| phonics_scheme_phase_id | int | no | no |
| name | text | no | no |
| Focus | text | no | no |
| Description | text | no | no |
| scheme_order | int | no | no |

Relationships:
- belongs_to → phonics_scheme_phase

Indexes:
- primary (id)

---

## Table: phonics_scheme
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| name | text | no | no |
| description | text | no | no |
| status | enum() | no | no |

Indexes:
- primary (id)

---

## Table: phonics_scheme_phase
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| phonics_scheme_id | int | no | yes |
| name | text | no | no |
| focus | text | no | no |
| description | text | no | no |

Relationships:
- belongs_to → phonics_scheme

Indexes:
- primary (id)

---

## Table: phonics_stage_exceptions
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| phonics_exceptions_id | int | no | no |
| phonics_phase_stage_id | int | no | no |
| active | bool | no | no |
| created_at | timestamp | no | yes |

Relationships:
- belongs_to → phonics_exceptions
- belongs_to → phonics_phase_stage

Indexes:
- primary (id)

---

## Table: phonics_stage_grapheme
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| phonics_grapheme_id | int | no | no |
| phonics_phase_stage_id | int | no | no |
| active | bool | no | no |
| created_at | timestamp | no | no |

Relationships:
- belongs_to → phonics_grapheme
- belongs_to → phonics_phase_stage

Indexes:
- primary (id)
- btree (created_at)

---

## Table: products
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| Name | text | no | no |
| status | enum(active, inactive, deprecated, test) | no | no |
| amount | int | no | no |
| Description | text | no | no |
| Type | text | no | no |
| stripe_id | text | no | no |
| stripe_price_test | text | no | no |
| stripe_product_live | text | no | no |
| stripe_price_live | text | no | no |
| Date_UTC | timestamp | no | yes |
| Statement_Descriptor | text | no | no |
| Unit_Label | text | no | no |
| Url | text | no | no |
| Tax_Code | text | no | no |
| currency | text | no | no |
| print_specification | json | no | no |
| papermill_template_id_cover | text | no | no |
| papermill_template_id_inner | text | no | no |
| last_modified_date | timestamp | no | yes |
| created_date | timestamp | no | yes |

Relationships:
- belongs_to → stripe

Indexes:
- primary (id)

---

## Table: shipping_options
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| created_at | timestamp | no | no |
| name | text | no | no |
| description | text | no | no |
| amount | int | no | no |

Indexes:
- primary (id)
- btree (created_at)

---

## Table: store_order_updates
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| store_orders_id | int | no | no |
| message | text | no | no |
| created_at | timestamp | no | no |

Relationships:
- belongs_to → store_orders

Indexes:
- primary (id)
- btree (created_at)

---

## Table: store_orders
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| order_number | text | no | no |
| message | text | no | no |
| instant_stories_id | int | no | no |
| size | text | no | no |
| orientation | text | no | no |
| products_id | int | no | no |
| status | enum(Payment Pending, Payment Confirmed, Order Confirmed, In Production, Order Confirmed, Delivered, Cancelled, Error) | no | no |
| payment_status | enum(Pending, Confirmed, Refunded, Cancelled, Error) | no | no |
| shipping | text | no | no |
| subtotal | decimal | no | no |
| shipping_amount | decimal | no | no |
| shipping_name | text | no | no |
| shipping_phone | text | no | no |
| shipping_email | text | no | no |
| shipping_add_full | text | no | no |
| shipping_add1 | text | no | no |
| shipping_add2 | text | no | no |
| shipping_town | text | no | no |
| shipping_postcode | text | no | no |
| locale_data_id | int | no | no |
| users_id | int | no | no |
| checkout_session_id | text | no | no |
| checkout_session_object | json | no | no |
| cover_pdf | attachment | no | yes |
| inner_pdf | attachment | no | yes |
| hpbc_order_id | text | no | no |
| hpbc_lock | bool | no | no |
| created_at | timestamp | no | no |
| last_modified_at | timestamp | no | yes |

Relationships:
- belongs_to → instant_stories
- belongs_to → products
- belongs_to → locale_data
- belongs_to → users
- belongs_to → checkout_session
- belongs_to → hpbc_order

Indexes:
- primary (id)
- btree (created_at)

---

## Table: subscriptions
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| name | text | no | no |
| status | enum(Active, Inactive) | no | no |
| billing_frequency | enum(Monthly, Annual) | no | no |
| default_payment_method | int | no | no |
| stripe_subscription_id | text | no | no |
| plans_id | int | no | no |
| transactions_id | int | no | no |
| current_period_start | date | no | yes |
| current_period_end | date | no | yes |
| cancel_at | date | no | yes |
| cancel_at_period_end | date | no | yes |
| cancelled_at | date | no | yes |
| ended_at | date | no | yes |
| created_at | timestamp | no | no |
| last_modified_at | timestamp | no | yes |

Relationships:
- belongs_to → stripe_subscription
- belongs_to → plans
- belongs_to → transactions

Indexes:
- primary (id)
- btree (created_at)

---

## Table: support_requests
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| name | text | no | no |
| description | text | no | no |
| users_id | int | no | no |
| Category | enum(Technical Support, Store, Report a bug, Product Feedback, Other) | no | no |
| status | enum(Pending, Working On It, Resolved) | no | no |
| owner | int | no | no |
| created_at | timestamp | no | no |
| last_modified_at | timestamp | no | yes |

Relationships:
- belongs_to → users

Indexes:
- primary (id)
- btree (created_at)

---

## Table: themes
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| name | text | no | no |
| description | text | no | no |
| image_keywords | text | no | no |
| google_font | text | no | no |
| access_tier | enum(Free, Premium) | no | no |
| plan_level | int | no | no |
| status | enum(Active, Inactive) | no | no |
| is_new | bool | no | no |
| theme_story_count | int | no | no |
| upvote_count | int | no | no |
| instant_stories_id | int | no | no |
| created_at | timestamp | no | no |
| last_modified_at | timestamp | no | yes |

Relationships:
- belongs_to → instant_stories

Indexes:
- primary (id)
- btree (created_at)

---

## Table: token_usage
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| users_id | int | no | no |
| entity | enum(instant_story, instant_story_page, character) | no | no |
| entity_id | int | no | no |
| image_jobs_id | int | no | no |
| type | enum(story_text, story_image, character_image, content_moderation) | no | no |
| input_tokens | int | no | no |
| output_tokens | int | no | no |
| total_tokens | int | no | no |
| estimated_cost_usd | decimal | no | no |
| provider | text | no | no |
| model | text | no | no |
| result | enum(success, error) | no | no |
| attempt_number | int | no | no |
| created_at | timestamp | no | no |
| completed_at | timestamp | no | yes |

Relationships:
- belongs_to → users
- belongs_to → entity
- belongs_to → image_jobs

Indexes:
- primary (id)
- btree (created_at)

---

## Table: transaction_webhook_events
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| status | enum() | no | no |
| processing_errors | text | no | no |
| external_id | text | no | no |
| data | attachment | no | yes |
| created_at | timestamp | no | no |
| last_modified_at | timestamp | no | yes |

Relationships:
- belongs_to → external

Indexes:
- primary (id)
- btree (created_at)

---

## Table: transactions
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| name | text | no | no |
| price | decimal | no | no |
| status | enum() | no | no |
| transaction_webhook_events_id | int | no | no |
| created_at | timestamp | no | no |
| last_modified_at | timestamp | no | yes |

Relationships:
- belongs_to → transaction_webhook_events

Indexes:
- primary (id)
- btree (created_at)

---

## Table: user_activities
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| created_at | timestamp | no | no |
| activities_id | int | no | no |
| users_id | int | no | no |
| last_modified_at | timestamp | no | yes |
| completed_at | timestamp | no | yes |

Relationships:
- belongs_to → activities
- belongs_to → users

Indexes:
- primary (id)
- btree (created_at)

---

## Table: user_alerts
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| message | text | no | no |
| type | enum(Content Moderation, System, Rewards) | no | no |
| is_read | bool | no | no |
| users_id | int | no | no |
| created_at | timestamp | no | no |

Relationships:
- belongs_to → users

Indexes:
- primary (id)
- btree (created_at)

---

## Table: user_logs
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| event_type | enum(Auth - Sign Up, Auth - Login, Character - Create, Character - Edit, Character - Update Image, Instant Story - Create, Instant Story - Edit, Instant Story - Completed, Instant Story - Delete, Support - Create) | no | no |
| users_id | int | no | no |
| user_sessions_id | int | no | no |
| metadata | object | no | no |
| created_at | timestamp | no | no |

Relationships:
- belongs_to → users
- belongs_to → user_sessions

Indexes:
- primary (id)
- btree (created_at)

---

## Table: user_sessions
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| users_id | int | no | no |
| device_label | text | no | yes |
| platform | text | no | no |
| app_version | text | no | no |
| status | enum(active, expired) | no | no |
| refresh_token | password | no | no |
| created_at | timestamp | no | no |
| last_modified_at | timestamp | no | yes |
| expires_at | timestamp | no | yes |

Relationships:
- belongs_to → users

Indexes:
- primary (id)
- btree (created_at)

---

## Table: user_child_profiles
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | uuid | yes | no |
| name | text | no | no |
| users_id | int | no | no |
| created_at | timestamp | no | no |

Relationships:
- belongs_to → users

Indexes:
- primary (id)
- btree (created_at)

---

## Table: users
Type: system_or_reference

| Field | Type | Required | Nullable |
|------|------|----------|----------|
| id | int | yes | no |
| username | text | yes | no |
| email | email | yes | yes |
| password | password | yes | yes |
| first_name | text | no | no |
| last_name | text | no | no |
| full_name | text | no | no |
| about_me | text | no | no |
| profile_photo | image | no | yes |
| rewards_balance | int | no | no |
| stripe_customer_id | text | no | no |
| stripe_test_customer_id | text | no | no |
| locale_data_id | int | no | no |
| instant_stories_id | int | no | no |
| stories_id | int | no | no |
| subscription_active | bool | no | no |
| plan_level | int | no | no |
| subscriptions_id | int | no | no |
| orders_id | int | no | no |
| email_verified | bool | no | no |
| onboarding_complete | bool | no | no |
| magic_link | object | no | yes |
| temp_login | object | no | no |
| temp_token_used | bool | no | no |
| created_at | timestamp | no | no |
| last_modified_at | timestamp | no | yes |
| last_login | timestamp | no | yes |
| test_mode | bool | no | no |
| mixpanel_user_uuid | uuid | no | yes |
| stories_total | int | no | no |
| preferences | object | no | no |

Relationships:
- belongs_to → stripe_customer
- belongs_to → stripe_test_customer
- belongs_to → locale_data
- belongs_to → instant_stories
- belongs_to → stories
- belongs_to → subscriptions
- belongs_to → orders

Indexes:
- primary (id)
- btree (created_at)
- unique (email)

---

