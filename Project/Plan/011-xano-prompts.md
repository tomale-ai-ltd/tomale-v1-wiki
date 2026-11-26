---
type: plan
title: "011 make a story: Xano AI prompts (X1–X12) and Postman folder 9"
project: tomale-rn-v1
status: draft
date: 2026-11-24
last_verified: 2026-11-26
related:
  - "[[011-story-creation-micro-prd]]"
  - "[[PRD-Chatbot-Story-Conversations]]"
  - "[[story-creation-flow]]"
  - "[[content-moderation-policy-v1.0]]"
---

# 011: Xano AI prompts

Paste one at a time, in order. Send Claude the Xano AI's summary (or the code) before publishing each. Refusals follow 009: `inputerror` (400) with `payload: {code, message}`; not-found is 404 with `payload.code`. Strict comparisons everywhere.

Rewritten 26/11 (Kyle): every story has a server-written conversation log, the idea is moderated when it's confirmed, a new `safeguarding_concern` outcome for possible disclosures, and moderation strikes, in line with the internal content moderation policy §4 (silent flagging, evidence preservation).

Order: X1–X4 first (the app can start on them), then X5–X7, then X8–X12, all before the phone pass. Before X5, set two environment variables: `SAFEGUARDING_ALERT_EMAIL` (where review alerts go; Kyle's work address) and `STORY_MONTHLY_LIMIT` (default 4). Mark your own test accounts `test_mode` so the cap doesn't stop testing.

## X1: schema
```
Schema change only. Don't change any endpoint or function.
1. Table "instant_stories": add
   - phonics_phase_stage_id (int, nullable, references phonics_phase_stage)
   - generation_started_at (timestamp, nullable)
   - blocked_kind (enum: content, safeguarding; nullable)
2. Table "moderation_flags": show me its current columns first. It must end up with (add what's missing, keep what's there):
   users_id (int), user_profiles_id (uuid, nullable), instant_stories_id (int, nullable), conversations_id (int, nullable),
   kind (enum: strike, flag_account, safeguarding), stage (enum: idea, surprise, page_text),
   flagged_text (text), enforcement (text), reason (text),
   created_at (timestamp), reviewed_at (timestamp, nullable), review_note (text, nullable).
   No API endpoint may read or write this table. Request history off for it.
3. Table "conversations": chat_messages is object[] with items {role, content, created_at}. Keep those and add optional item fields: step (text), type (text), profile_id (uuid), data (json). Existing rows stay valid.
```

## X2: the story log function
```
Create a custom function story/log_event. Inputs: int instant_stories_id, text step, text type, json data. Change nothing else.
Also input text content (optional, the display text).
1. Find the conversation with instant_stories_id = input and conversation_type = "story". If none, create it (users_id from the story, status "active", chat_messages []).
2. Append one item to chat_messages: {role, content, created_at: now, step, type, profile_id: the story's user_profiles_id, data}. role is "assistant" for ideas_offered, suggestions and surprise; "system" for moderation and safeguarding; "user" for everything else. content is the display text (the idea, or a short label such as "Pip and Rosie"); empty for moderation and safeguarding.
3. Update last_modified_at. Return nothing.
Event types used: idea (data {text}), ideas_offered ({ideas}), suggestions ({characters_ids, theme_id}), surprise ({user_prompt, characters_ids, theme_id, artwork_style_id}), characters ({characters_ids}), theme ({theme_id}), style ({artwork_style_id}), phonics ({phonics_phase_stage_id}), make ({}), moderation ({outcome}), safeguarding ({}).
This function is only ever called by other functions and endpoints; the app can never write events.
Set request history to disabled for this function (it carries children's free text).
```

## X3: create and edit a draft
```
Two changes in the app API group. Change nothing else.

A. POST /instant_stories
1. Remove these inputs entirely: approved_by_profile_id, approved_at, approval_rejected_at.
2. Remove user_prompt as an input too (the idea is only set through POST /instant_stories/{id}/idea, so every version is moderated). Keep title, subtitle, theme_id, artwork_style_id optional; add optional int phonics_phase_stage_id.
3. Ignore any client total_pages: always total_pages = 12 (page shells as today).
4. Before db.add: load the user for $auth.id; email_verified !== true → inputerror payload {code "EMAIL_NOT_VERIFIED", message "Please confirm your email first."}.
5. users_id and user_profiles_id from the token as today; status = "Draft".
6. After db.add, create the conversation (conversation_type "story", instant_stories_id, users_id, status "active", chat_messages []) and return the story plus conversation_id.

B. New PATCH /instant_stories/{id}. Authentication required (users).
Inputs (all optional): int theme_id, int artwork_style_id, int phonics_phase_stage_id (nullable: null clears it). No user_prompt.
1. Load the story with the same ownership and active-profile rule as GET /instant_stories/{id} (a child may only edit its own story; a parent any story on the account). Not visible → 404 payload {code "STORY_NOT_FOUND"}.
2. status !== "Draft" → inputerror payload {code "STORY_NOT_EDITABLE", message "This story is already being made."}.
3. Given ids must exist (theme and style active) → otherwise inputerror payload {code "INVALID_INPUT", message "That choice isn't available."}.
4. db.edit only the inputs sent, plus last_modified_at = now.
5. For each input sent, function.run story/log_event (step "theme" / "style" / "phonics", same type, data with the id).
6. Return the same shape as GET /instant_stories/{id}.
```

## X4: choose characters (check the existing endpoint)
```
POST /instant_stories/{instant_stories_id}/characters already exists (input characters_ids). Show me the current code, then make it match:
1. Ownership and active-profile rule as PATCH /instant_stories/{id}; status !== "Draft" → STORY_NOT_EDITABLE.
2. characters_ids: 1 to 3 ids, each a character on this account, not deleted or archived → otherwise inputerror payload {code "INVALID_CHARACTERS", message "Please choose one to three characters."}.
3. Replace the story's set: delete its instant_story_characters rows, add one per id. Never edit a character record.
4. function.run story/log_event (step "characters", type "characters", data {characters_ids}).
5. Return {characters: [{id, name, cover_image}]}.
```

## X5: moderation with safeguarding and strikes
```
Two functions. Show me content_moderation_story_text first.

A. Update the moderation prompt and schema used by content_moderation_story_text:
- Add the enforcement value "safeguarding_concern", for text that reads like the writer (a child or an adult) disclosing that something harmful is happening to them or that they may hurt themselves: being hurt, touched inappropriately, threatened, kept secret, frightened at home, wanting to die or self-harm. This is about the person telling us something about their own life, not a story theme (a story about a dragon who is scared is "none").
- Keep none, require_parental_oversight, blocked, flag_account exactly as they are.
- Add an else branch: any unrecognised value is treated as "blocked" (fail closed; known gap in story-creation-flow).

B. New custom function moderation/check_idea. Inputs: int instant_stories_id, text text, text stage (idea | surprise | page_text). Returns {outcome}.
1. Run the same moderation prompt on the text (plus the story's character names), with whether the active profile is a child.
2. none or require_parental_oversight → return {outcome: "ok"} (parental oversight is applied later by page_text as today).
3. blocked → add a moderation_flags row (kind "strike", stage, flagged_text = text, enforcement, reason, ids); function.run story/log_event (type "moderation", data {outcome: "blocked"}); then the strike rule (step 6); return {outcome: "blocked"}.
4. flag_account → as blocked, but kind "flag_account", and send the review email (step 7); return {outcome: "blocked"}.
5. safeguarding_concern → add a moderation_flags row (kind "safeguarding", same fields); function.run story/log_event (type "safeguarding", data {}); send the review email (step 7); return {outcome: "safeguarding"}. Don't count it as a strike. Don't alert the parent or create any user_alert.
6. Strike rule: if this account has 3 or more kind "strike" rows in the last 30 days and no kind "flag_account" row in that time, add a kind "flag_account" row (reason "repeated attempts") and send the review email. Never tell the user.
7. Review email: Resend to the address returned by function safeguarding/alert_recipient (step 8), subject "Tomale review needed: <kind>", body with only the moderation_flags id, kind and time. No story text, names or email addresses in the email.
8. Create a custom function safeguarding/alert_recipient with input int users_id. For now it returns $env.SAFEGUARDING_ALERT_EMAIL and ignores users_id. Every review email gets its recipient from this function, never from the env var directly (so a school's safeguarding lead can be added later in one place).
```

## X6: confirm the idea
```
New POST /instant_stories/{id}/idea. Authentication required (users). Input: text user_prompt filters=trim, required, max 300.
1. Ownership and active-profile rule as PATCH; status !== "Draft" → STORY_NOT_EDITABLE.
2. function.run story/log_event (step "idea", type "idea", data {text: user_prompt}) (every version is logged, including refused ones).
3. function.run moderation/check_idea (stage "idea").
   - "blocked" → inputerror payload {code "CONTENT_REJECTED", message "Let's try a different idea."}. Don't save the prompt.
   - "safeguarding" → inputerror payload {code "SAFEGUARDING_CONCERN", message "It sounds like something might be worrying you."}. Don't save the prompt.
4. Save user_prompt on the story (last_modified_at = now).
5. Suggestions: call the model through a new data_models record "story-suggest" (same text model as story-text, strict structured output) with the idea, the account's characters (id, name, physical description; not deleted or archived) and the active themes (id, name, description).
   System prompt: "Given a child's story idea, pick which of the household's characters it is about and which theme fits best. Only use ids from the lists given. If the idea names or clearly describes a character (e.g. 'the dragon' when the household has one dragon), include it. At most 3 characters. If nothing fits, return an empty list and null."
   Output {characters_ids: [int], theme_id: int or null}. Drop ids that aren't the account's or an active theme; if two kept characters share a name, keep only the most recently created.
   If the model call fails, return empty suggestions (the prompt is still saved).
6. function.run story/log_event (type "suggestions", data as returned).
7. Return {user_prompt, characters_ids, theme_id}.
```

## X7: ideas and Surprise me
```
Two new endpoints, both authenticated, both with the ownership rule and status === "Draft" (else STORY_NOT_EDITABLE), both rate limited together with /idea's suggestion call: at most 20 AI calls per account per hour → payload {code "RATE_LIMITED", message "Please wait a minute and try again."} (same HTTP status as RATE_LIMITED elsewhere).
Context for both: the account's characters (name and physical description, newest 20), the titles and themes of the active profile's 5 most recent stories (not Draft), and whether the active profile is a child. Names and creative content only.

A. POST /instant_stories/{id}/ideas. Uses a new data_models record "story-ideas" (same model as story-text).
System prompt: "You suggest short story ideas for a personalised picture book for a child aged 3 to 8. Ideas are gentle, kind and age-appropriate: no violence, fear beyond mild suspense, romance, brands, real people or scary illness. Use the characters' names. Each idea is one sentence of at most 25 words, plus a short title of at most 6 words. Don't repeat the recent stories."
Output (strict) {ideas: [{title, idea}]}, exactly 3. Log (type "ideas_offered"). Return {ideas}. Nothing saved on the story.

B. POST /instant_stories/{id}/surprise. Uses "story-suggest" with a surprise instruction: one idea (one sentence, at most 40 words), 1 to 3 of the household's characters and one theme, different from the recent stories.
Validate ids as in X6 step 5; if no valid character is left, use the most recently created character. artwork_style_id: the active profile's most recent story's style if still active, else the first active style.
function.run moderation/check_idea on the idea (stage "surprise"); blocked → try once more, then inputerror CONTENT_REJECTED.
Save on the story: user_prompt, theme_id, artwork_style_id, and the character set (as X4 step 3). Log (type "surprise"). Return {user_prompt, characters_ids, theme_id, artwork_style_id}.
```

## X8: page_text: email gate, monthly cap, safeguarding
```
Change POST /instant_stories/{id}/page_text (and generate_story_page_text only where needed). Change nothing else.
When the story's status === "Draft", before anything else:
1. email_verified !== true → inputerror payload {code "EMAIL_NOT_VERIFIED"}.
2. Unless users.test_mode === true: count this account's instant_stories with generation_started_at on or after the start of this calendar month (Europe/London) and status in ["Preparing", "In Queue", "Done"]. If count >= $env.STORY_MONTHLY_LIMIT (default 4) → inputerror payload {code "ENTITLEMENT_LIMIT_REACHED", message "This month's stories are used up.", resets_at: <start of next month, Europe/London, epoch ms>}. The story stays Draft.
3. generation_started_at = now; function.run story/log_event (type "make").
4. Carry on as today. In content_moderation_story_text's outcomes: blocked and flag_account also set blocked_kind = "content" and add the moderation_flags row as in X5 (stage "page_text"); safeguarding_concern sets status "Blocked", status_moderation "Fail", blocked_kind "safeguarding", and does X5 B step 5.
5. If text generation rolls the story back to Draft, set generation_started_at = null.
When the story isn't Draft, return its current {id, status, status_moderation, blocked_kind} with HTTP 200 instead of an empty body.
```

## X9: allowance
```
New GET /story_allowance. Authentication required (users). No inputs.
Return {used, limit, resets_at}: the same count as X8 step 2, limit = STORY_MONTHLY_LIMIT (default 4), resets_at as in X8.
```

## X10: lists for Story builder and Being made
```
Change GET /instant_stories (list). Keep approval_state, child redaction and rejected filtering exactly as they are.
1. status === "Draft": only the active profile's own drafts that have a user_prompt (empty drafts are never listed), newest last_modified_at first.
2. New optional bool in_progress: when true, the active profile's stories with status in ["Preparing", "In Queue"], newest first.
3. Each item also returns total_pages, images_remaining, theme {id, name}, characters [{id, name, cover_image}], last_modified_at, blocked_kind.
```

## X11: phonics in generation and on the story
```
Change generate_story_page_text and GET /instant_stories/{id}. Change nothing else.
1. When phonics_phase_stage_id is set, run phonics_graphemes_up_to_stage and phonics_exceptions_up_to_stage and append to the story-text user prompt: "Phonics focus: where you can, use words built from these graphemes: <list>. Include these tricky words at least once each: <list>. Keep sentences short and simple." Unset: the prompt is exactly as today.
2. GET /instant_stories/{id}: return blocked_kind, and phonics: null when unset, else {scheme {id, name}, phase {id, name}, stage {id, name}, graphemes [{grapheme, example}] (this stage's own, from the per-stage function; example null if none), tricky_words [text] (this stage's own)}. Keep phonics_phase_stage_id.
```

## X12: the conversation for resuming, and clean-ups
```
1. New GET /instant_stories/{id}/conversation. Same ownership and active-profile rule as GET /instant_stories/{id}. Return {events: [{step, type, role, content, data, created_at}]} from chat_messages, with only these types, in order: idea (the latest version only), ideas_offered (the latest only), suggestions (latest), surprise, characters, theme, style, phonics, make. Never return moderation or safeguarding events, refused idea versions, moderation_flags data or profile ids.
2. POST /conversations and DELETE /conversations/{id}: remove the chat_messages, status, last_modified_at, is_deleted and deleted_at inputs from POST (the app must not write conversation content). Leave GET as is. These endpoints stay for character chat (M6a).
3. GET /artwork_style (list and single): stop returning image_prompt_positive and image_prompt_negative.
```

## Postman folder 9 (Make a story)

Gate with env `runStoryCreateTests`. Use a confirmed `test_mode` account, a second unconfirmed account (9A-1) and a confirmed non-test account (9E). Set `SAFEGUARDING_ALERT_EMAIL` to your own address before 9F.

- **9A Draft:** 9A-1 unconfirmed `POST /instant_stories` → `EMAIL_NOT_VERIFIED`; 9A-2 confirmed `POST /instant_stories {}` → Draft, `total_pages` 12, a `conversation_id`, approval fields and `user_prompt` ignored if sent; 9A-3 `?status=Draft` doesn't list it yet (no idea); 9A-4 characters 0 ids / 4 ids / another account's id → `INVALID_CHARACTERS`; 9A-5 two good ids → 200; 9A-6 `PATCH` theme, style, phonics stage → 200 and `GET` shows them with `phonics` filled; 9A-7 `PATCH` a missing theme → `INVALID_INPUT`.
- **9B Idea and AI help:** 9B-1 `POST …/idea` naming one of the account's characters → saved, that id in `characters_ids`, an active `theme_id`; 9B-2 `?status=Draft` now lists it; 9B-3 `POST …/ideas` → 3 ideas; 9B-4 `POST …/surprise` on a new draft → prompt, 1–3 character ids, theme and style saved on the story; 9B-5 the 21st AI call in an hour → `RATE_LIMITED` (by hand).
- **9C Moderation:** 9C-1 `…/idea` with a clearly disallowed idea → `CONTENT_REJECTED`, prompt not saved, a `strike` row (check in the database); 9C-2 three refusals in a row on one account → a `flag_account` row and one review email; 9C-3 `…/idea` with a test disclosure sentence (e.g. "my uncle hurts me and says it's a secret") → `SAFEGUARDING_CONCERN`, a `safeguarding` row, a review email with no story text, no user_alert created; 9C-4 `GET …/conversation` shows neither the refused versions nor any moderation event.
- **9D Make it:** 9D-1 `POST …/page_text` → In Queue (or Preparing), `generation_started_at` set; 9D-2 `PATCH` now → `STORY_NOT_EDITABLE`; 9D-3 `?in_progress=true` lists it with `images_remaining`; 9D-4 `page_text` again → 200 with the current status; 9D-5 `GET …/conversation` ends with a `make` event.
- **9E Cap:** with `STORY_MONTHLY_LIMIT` set to the non-test account's current count, `page_text` on a new draft → `ENTITLEMENT_LIMIT_REACHED` with `resets_at`, story still Draft; `GET /story_allowance` matches. (By hand: set the env var, run, set it back.)
- **9F Phonics:** a story with a stage reaches In Queue and the request history shows the phonics block in the story-text prompt.

## Later (not 011)

- `story/log_event` reads, appends and writes `chat_messages`, so two simultaneous events on one story could lose one (accepted 26/11; the app calls are sequential). If the log is ever relied on as evidence at volume, move it to an append-only `story_events` table (one row per event).

- The purge job (M7) must not delete moderation_flags rows or the stories and conversations they point to; they're kept for the period the solicitor sets ([[pre-launch-checklist]] §6). Empty drafts (no idea) older than a day are deleted by it.
- Locked art styles and the real plan limits replace `STORY_MONTHLY_LIMIT` in M8.
- The other known gaps in [[story-creation-flow]] (double page_text, `debug.stop` 200s, the `flag_account` branch storing a null prompt) stay on the pre-launch list; X5's fail-closed branch closes one of them.
