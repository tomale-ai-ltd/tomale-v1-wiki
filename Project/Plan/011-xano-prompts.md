---
type: plan
title: "011 make a story: Xano AI prompts (X1–X9) and Postman folder 9"
project: tomale-rn-v1
status: draft
date: 2026-11-24
related:
  - "[[011-story-creation-micro-prd]]"
  - "[[PRD-Chatbot-Story-Conversations]]"
  - "[[story-creation-flow]]"
---

# 011: Xano AI prompts

Paste one at a time, in order. Send Claude the Xano AI's summary (or the code) before publishing each. Refusals follow 009: `inputerror` (400) with `payload: {code, message}`; not-found is 404 with `payload.code`. Strict comparisons everywhere.

The app can start once X1–X3 are published. X4–X7 are needed before the phone pass; X8–X9 are small clean-ups.

## X1: schema
```
Schema change only. Don't change any endpoint or function.
Table "instant_stories":
- add phonics_phase_stage_id (int, nullable, references phonics_phase_stage)
- add generation_started_at (timestamp, nullable)
```

## X2: create and edit a draft
```
Two changes in the app API group. Change nothing else.

A. POST /instant_stories
1. Remove these inputs entirely: approved_by_profile_id, approved_at, approval_rejected_at (the client must never set approval fields).
2. Make every remaining input optional so an empty draft can be created: title, subtitle, user_prompt, theme_id, artwork_style_id. Add optional int phonics_phase_stage_id.
3. Ignore any client total_pages: always set total_pages = 12 (the page shells are created from it as today).
4. Before db.add: load the user for $auth.id; email_verified !== true → inputerror payload {code "EMAIL_NOT_VERIFIED", message "Please confirm your email first."}.
5. Keep users_id and user_profiles_id from the token exactly as today; status = "Draft".

B. New PATCH /instant_stories/{id}. Authentication required (users).
Inputs (all optional): int theme_id, int artwork_style_id, text user_prompt filters=trim max 300, int phonics_phase_stage_id (nullable: sending null clears it).
1. Load the story with the same ownership and active-profile rule as GET /instant_stories/{id} (owner $auth.id; a child may only edit its own story; a parent may edit any story on the account). Not visible → 404 payload {code "STORY_NOT_FOUND"}.
2. status !== "Draft" → inputerror payload {code "STORY_NOT_EDITABLE", message "This story is already being made."}.
3. theme_id, artwork_style_id and phonics_phase_stage_id, when given, must exist (and theme/style be active) → otherwise inputerror payload {code "INVALID_INPUT", message "That choice isn't available."}.
4. db.edit only the inputs that were sent, plus last_modified_at = now.
5. Return the same shape as GET /instant_stories/{id}.
```

## X3: choose characters (check the existing endpoint)
```
POST /instant_stories/{instant_stories_id}/characters already exists (input characters_ids). Check it and change it only where it differs from this:
1. Same ownership and active-profile rule as PATCH /instant_stories/{id}; status !== "Draft" → STORY_NOT_EDITABLE.
2. characters_ids: 1 to 3 ids, each a character on this account ($auth.id), not deleted and not archived. Otherwise inputerror payload {code "INVALID_CHARACTERS", message "Please choose one to three characters."}.
3. It replaces the story's set: delete the story's instant_story_characters rows, then add one per id. It never edits a character record.
4. Return {characters: [{id, name, cover_image}]}.
Show me the current code before changing anything.
```

## X4: story ideas
```
Two parts.

A. Create a data_models record like the existing story-text record, type "story-ideas", using the same text model and settings as story-text for now.
System prompt: "You suggest short story ideas for a personalised picture book for a child aged 3 to 8. Ideas are gentle, kind and age-appropriate: no violence, fear beyond mild suspense, romance, brands, real people or scary illness. Use the characters' names. Each idea is one sentence of at most 25 words, plus a short title of at most 6 words."
Structured output (strict): {ideas: [{title: string, idea: string}]} with exactly 3 items.

B. New POST /instant_stories/{id}/ideas. Authentication required (users). No inputs besides the id.
1. Same ownership and active-profile rule as PATCH /instant_stories/{id}; status !== "Draft" → STORY_NOT_EDITABLE.
2. Rate limit: at most 10 calls per story per hour (store a counter on the story or use the existing rate-limit pattern) → inputerror payload {code "RATE_LIMITED", message "Please wait a minute and try again."} (HTTP 429 if that's how RATE_LIMITED is returned elsewhere).
3. Build the user prompt from: the story's characters (name and physical description), the theme name and description (if set), the art style name (if set), and whether the active profile is a child. Names and creative content only, nothing else about the family.
4. Call the model through the story-ideas record, record token_usage like story-text does.
5. Return {ideas: [{title, idea}]}. Don't save the ideas on the story.
```

## X5: monthly cap and the email gate on page_text
```
Change POST /instant_stories/{id}/page_text (and the generate_story_page_text function only where step 4 needs it). Change nothing else.
Before anything else runs, and only when the story's status === "Draft":
1. Load the user for $auth.id. email_verified !== true → inputerror payload {code "EMAIL_NOT_VERIFIED", message "Please confirm your email first."}.
2. Unless users.test_mode === true: count this account's instant_stories with generation_started_at on or after the start of the current calendar month (Europe/London) and status in ["Preparing", "In Queue", "Done"]. If count >= the environment variable STORY_MONTHLY_LIMIT (default 4 if unset) → inputerror payload {code "ENTITLEMENT_LIMIT_REACHED", message "This month's stories are used up.", resets_at: <start of next month, Europe/London, epoch ms>}. The story stays Draft.
3. Set generation_started_at = now on the story, then carry on exactly as today.
4. If text generation rolls the story back to Draft, also set generation_started_at = null, so a failed story doesn't use the allowance.
Blocked stories don't count (step 2's status list).
```

## X6: allowance
```
New GET /story_allowance in the app API group. Authentication required (users). No inputs.
Return {used, limit, resets_at}: used is the same count as page_text's cap (X5 step 2), limit is STORY_MONTHLY_LIMIT (default 4), resets_at as in X5. For a test_mode user return the same numbers (the app only displays them).
```

## X7: lists for Story builder and Being made
```
Change GET /instant_stories (list) in the app API group. Change nothing about approval_state, child redaction or rejected-story filtering.
1. When status === "Draft" is requested: return only drafts whose user_profiles_id is the active profile's (a parent sees its own drafts here, not the children's), newest last_modified_at first.
2. Add optional bool in_progress: when true, return only the active profile's stories with status in ["Preparing", "In Queue"], newest first.
3. Each list item also returns total_pages, images_remaining, theme {id, name}, characters [{id, name, cover_image}] and last_modified_at (if not already).
```

## X8: phonics in the generation prompt
```
Change generate_story_page_text only. Change nothing else.
When the story's phonics_phase_stage_id is set:
1. Run phonics_graphemes_up_to_stage and phonics_exceptions_up_to_stage for that stage.
2. Append to the story-text user prompt: "Phonics focus: where you can, use words built from these graphemes: <list>. Include these tricky words at least once each: <list>. Keep sentences short and simple."
When it isn't set, the prompt is exactly as today.
Also return phonics_phase_stage_id and the stage's name on GET /instant_stories/{id}.
```

## X9: small clean-ups
```
1. GET /artwork_style (list and single): stop returning image_prompt_positive and image_prompt_negative to the app.
2. POST /instant_stories/{id}/page_text: when the story isn't Draft, return its current {id, status, status_moderation} with HTTP 200 instead of an empty body, so the app can tell where it is.
```

## Postman folder 9 (Make a story)

Gate with env `runStoryCreateTests`. Use an existing confirmed test account (`test_mode` true) and a second, unconfirmed account for 9A-1.

- **9A Draft:** 9A-1 unconfirmed account `POST /instant_stories` → `EMAIL_NOT_VERIFIED`; 9A-2 confirmed `POST /instant_stories {}` → Draft, `total_pages` 12, no approval fields accepted (send `approved_at`, check it's null); 9A-3 characters 0 ids → `INVALID_CHARACTERS`; 9A-4 4 ids → `INVALID_CHARACTERS`; 9A-5 another account's character → `INVALID_CHARACTERS`; 9A-6 two good ids → 200, two characters; 9A-7 `PATCH` theme, style, prompt, phonics stage → 200 and `GET` shows them; 9A-8 `PATCH` with a missing theme id → `INVALID_INPUT`.
- **9B Ideas:** 9B-1 `POST …/ideas` → 3 ideas with title and idea; 9B-2 the 11th call in an hour → `RATE_LIMITED`.
- **9C Lists and allowance:** 9C-1 `?status=Draft` contains the draft; 9C-2 `GET /story_allowance` → numbers and a future `resets_at`.
- **9D Make it:** 9D-1 `POST …/page_text` → In Queue (or Preparing) and `generation_started_at` set; 9D-2 `PATCH` now → `STORY_NOT_EDITABLE`; 9D-3 `?in_progress=true` contains it with `images_remaining`; 9D-4 `POST …/page_text` again → 200 with the current status (X9).
- **9E Cap:** 9E-1 with `STORY_MONTHLY_LIMIT` set to the account's current count and a non-test account, `page_text` on a new draft → `ENTITLEMENT_LIMIT_REACHED` with `resets_at`, story still Draft. (Run by hand: set the env var, run, set it back.)
- **9F Phonics:** 9F-1 a story with a stage set reaches In Queue (check the request history shows the phonics block in the story-text prompt).

## Later (not 011)

- Draft clean-up: drafts untouched for 90 days are soft-deleted by the purge job (add to [[retain-account-data-30-days-after-closing]]'s task in M7; a PU when M7 is planned).
- Locked art styles and the real plan limits replace `STORY_MONTHLY_LIMIT` in M8 ([[PRD-Subscription-Entitlement-System]]).
- The known gaps in [[story-creation-flow]] (fail closed on an unknown moderation value, double page_text, `debug.stop` 200s) stay on the pre-launch list.
