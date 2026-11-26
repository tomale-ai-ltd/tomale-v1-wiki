---
type: plan
title: "Golden set v1 (IP-05)"
project: tomale-rn-v1
status: active
date: 2026-11-26
related:
  - "[[IP-05-golden-set]]"
  - "[[measure-character-consistency-with-a-vlm-judge-and-blind-ratings]]"
---

# Golden set v1

These are **frozen inputs only**: style, theme, prompt, synopsis, page text and character JSON for 12 stories (144 pages, 24 characters). `golden-set-v1.json` has sha256 `3fc315d944d382c091ad46f026783d4ec2cff43daabc89d46fa6f0d8cb168bd8`. It's rebuilt by `build_golden_set.py` from Kyle's Xano exports of 26/11 plus `authored.json`.

- **Baselines are regenerated**, not taken from the database. The harness runs today's pipeline (the default page and cover records with `gpt-image-2.6-flare`) and every candidate on the same inputs.
- **Character portraits are regenerated from the JSON.** Test-account characters may be modelled on family members, so their existing pictures aren't used.
- **Privacy:**
  - Only test accounts 66 and 135; no beta-tester stories.
  - Real-looking names are replaced throughout (Freya → Isla, Reuben → Theo, Noah → Finn, GG → Grandpa Bert, Reggie → Biscuit, Wilmslow → Willowbrook, Doris → Dot); the build fails if any remain.
  - A character resembling a copyrighted film character was dropped.
- **Assigned attributes:** where a character's JSON had no outfit, the set assigns one, marked `assigned_by_golden_set`, so the judge has something definite to check.
- **The JSON is the answer key** for the judge's attribute and bleed checks. Pip's JSON says only "cute postman outfit", so the colour exists only in his portrait. That's exactly the gap reference images close.

| ID | Style (tier 0) | Theme | Chars | Source | Tests |
|---|---|---|---|---|---|
| G01 | Pastel chalk | Action & Adventure | 1 | 648 | Outfit loss, same character on every page |
| G02 | Pastel chalk | Friendship | 3 linked, 2 in text | 576 | Linked characters not in the text stay out |
| G03 | Pastel chalk | Educational | 3 | 453 | Elderly man, toddler, dog |
| G04 | Coloured pencil | Action & Adventure | 3 | 464 | Three similar small children |
| G05 | Coloured pencil | Friendship | 1 | 564 | Cartoon animal with one distinctive feature |
| G06 | Anime | Friendship | 1 | 540 | Animal with accessories; second animal in text only |
| G07 | Blockbuster Animation | Superheroes | 2 | 603 | Detailed outfit; non-human villain |
| G08 | Blockbuster Animation | Action & Adventure | 2 | 451 | Child plus dog across the story |
| G09 | Blockbuster Animation | Bedtime | 1 | 448 | Colour-patterned creature |
| G10 | Polygon Art | Poetry & Rhyming | 2 | authored | Two animals whose outfits must not swap |
| G11 | Polygon Art | Educational | 1 | authored | In-scene text: LIBRARY, SCIENCE FAIR |
| G12 | Anime | Action & Adventure | 4 | authored | Identical twins differing only by colour (strongest bleed test) |

Tier 1 styles aren't included while they're inactive. If any come back for Creator at launch, add one story per style, as v1.1.
