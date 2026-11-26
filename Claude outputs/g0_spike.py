"""G0 child-image policy spike (Tomale image pipeline, task IP-02).

Generates stylised (non-photographic) storybook pages with child characters on
Vertex AI Gemini image models and records how often the safety filters block them.

Pass rule (PRD-Image-Pipeline §6): under 2% child-filter blocks on Gemini 3.1
Flash Image, `eu` endpoint.

Auth: your own gcloud login (Application Default Credentials). No keys.

Usage:
  python g0_spike.py --project tomale-image-dev --dry-run      # show the plan, no calls
  python g0_spike.py --project tomale-image-dev --limit 3      # smoke test, ~9 calls
  python g0_spike.py --project tomale-image-dev                # full run, ~165 calls

Docs checked 26/11/2026:
- Model IDs and locations: gemini-3.1-flash-image (global, us, eu);
  gemini-nano-banana-2.1 (global only).
- SDK: genai.Client(enterprise=True, project=..., location='eu').
- ImageConfig.person_generation: ALLOW_ALL | ALLOW_ADULT | ALLOW_NONE.
- Blocks: FinishReason IMAGE_SAFETY / IMAGE_PROHIBITED_CONTENT, PromptFeedback
  block reason, support codes in the message. Child codes 58061214 (input),
  17301594 (output); photorealistic celebrity/child 64151117.
"""

import argparse
import csv
import json
import random
import re
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

CHILD_CODES = {"58061214", "17301594", "64151117"}

TARGETS = {
    "eu-flash": ("eu", "gemini-3.1-flash-image"),
    "global-flash": ("global", "gemini-3.1-flash-image"),
    "global-nb21": ("global", "gemini-nano-banana-2.1"),
}

# Replace with the real tier 0/1 artwork_style descriptions via --styles styles.json
# (a JSON list of strings) for the most faithful result.
DEFAULT_STYLES = [
    "Soft 3D chibi illustration for a children's picture book: rounded shapes, big expressive eyes, "
    "gentle pastel lighting, smooth matte textures. Clearly an illustration, not a photograph.",
    "Warm watercolour picture-book illustration with soft edges, loose brushwork and a cosy palette. "
    "Clearly an illustration, not a photograph.",
    "Bright flat-colour cartoon illustration with clean outlines and simple shading, "
    "like a modern children's book. Clearly an illustration, not a photograph.",
]

CHARACTERS = [
    ("MIA", "a 6-year-old girl with curly red hair, freckles, a yellow raincoat and green wellies"),
    ("ARJUN", "a 7-year-old boy with short black hair, round glasses and a blue dinosaur hoodie"),
    ("ZOLA", "a 5-year-old girl with black hair in two puffs, purple dungarees and star hair clips"),
    ("OLLIE", "an 8-year-old boy with messy blond hair, a red football shirt and navy shorts"),
    ("LIN", "a 4-year-old girl with a black bob and fringe, a pink pinafore and white socks"),
]

SCENES = [
    ("hugging a teddy bear and yawning at bedtime", "a cosy bedroom with a night light and stars on the ceiling"),
    ("building a sandcastle with a bucket and spade", "a sunny beach with gentle waves"),
    ("jumping into a big puddle with a splash", "a rainy village street with colourful houses"),
    ("reading a book with a torch inside a blanket fort", "a living room at night"),
    ("feeding ducks with bread crumbs", "a calm park pond in spring"),
    ("dressed as a pirate holding a cardboard telescope", "a back garden with a washing-line sail"),
    ("planting seeds in a small pot", "a sunny greenhouse full of plants"),
    ("painting a rainbow at an easel", "a bright primary-school classroom"),
    ("whooshing down a hill on a red sledge", "a snowy hillside under a pale blue sky"),
    ("looking through a telescope at the moon", "a garden at night with fireflies"),
]

TWO_CHARACTER_SCENES = [
    "sharing a picnic blanket and laughing",
    "holding hands while crossing a little wooden bridge",
    "building a snowman together",
    "racing paper boats down a stream",
    "reading one big book together on a sofa",
]


def page_prompt(style, subject, background):
    return (
        f"STYLE: {style}\n\n"
        f"SUBJECT: {subject}\n\n"
        f"BACKGROUND: {background}\n\n"
        "COMPOSITION: medium shot, eye level, single clear focal point, soft depth of field.\n\n"
        "CONSTRAINTS: No additional characters. No collage or multiple panels. "
        "No text or lettering in the image. Storybook illustration, not a photograph."
    )


def build_plan(styles, limit):
    """Per target: 5 portraits, then 40 text-only pages, then 10 pages with labelled references."""
    plan = []
    for i, (name, desc) in enumerate(CHARACTERS):
        plan.append({
            "kind": "portrait", "id": f"portrait-{name}", "chars": [name], "refs": [],
            "aspect": "1:1",
            "prompt": page_prompt(styles[0], f"A friendly full-body character portrait of {name}, {desc}, smiling and waving.",
                                  "a plain soft pastel background"),
        })
    n = 0
    for c_idx, (name, desc) in enumerate(CHARACTERS):
        for s_idx, (action, background) in enumerate(SCENES):
            if (c_idx + s_idx) % 5 == 4:   # 40 of the 50 combinations
                continue
            n += 1
            style = styles[n % len(styles)]
            plan.append({
                "kind": "page-text", "id": f"text-{n:02d}", "chars": [name], "refs": [], "aspect": "3:2",
                "prompt": page_prompt(style, f"{name}, {desc}, {action}.", background),
            })
    for i, (name, desc) in enumerate(CHARACTERS):   # 5 single-reference pages
        action, background = SCENES[(i * 3) % len(SCENES)]
        plan.append({
            "kind": "page-ref1", "id": f"ref1-{name}", "chars": [name], "refs": [name], "aspect": "3:2",
            "prompt": page_prompt(styles[0], f"{name} (reference image 1), {action}. Keep {name} exactly as in reference image 1.", background),
        })
    for i, action in enumerate(TWO_CHARACTER_SCENES):   # 5 two-reference pages
        a, b = CHARACTERS[i], CHARACTERS[(i + 1) % len(CHARACTERS)]
        plan.append({
            "kind": "page-ref2", "id": f"ref2-{a[0]}-{b[0]}", "chars": [a[0], b[0]], "refs": [a[0], b[0]], "aspect": "3:2",
            "prompt": page_prompt(styles[0],
                                  f"{a[0]} (reference image 1) and {b[0]} (reference image 2) {action}. "
                                  f"{a[0]} looks exactly like reference image 1 and {b[0]} exactly like reference image 2; "
                                  "do not mix their hair, clothes or features.",
                                  "a sunny meadow"),
        })
    if limit:
        # smoke test: the first `limit` pages of each kind, plus only the portraits they need
        pages = []
        for kind in ("page-text", "page-ref1", "page-ref2"):
            pages += [it for it in plan if it["kind"] == kind][:limit]
        needed = {r for it in pages for r in it["refs"]} or {CHARACTERS[0][0]}
        plan = [it for it in plan if it["kind"] == "portrait" and it["chars"][0] in needed] + pages
    return plan


def make_client(project, location):
    from google import genai
    try:
        return genai.Client(enterprise=True, project=project, location=location)
    except TypeError:  # older SDKs
        return genai.Client(vertexai=True, project=project, location=location)


def classify(resp_dump, has_image, text):
    blob = json.dumps(resp_dump)
    codes = sorted(set(re.findall(r"\b\d{8}\b", blob)))
    finish = ""
    block = ""
    try:
        finish = str(resp_dump["candidates"][0].get("finish_reason") or "")
    except (KeyError, IndexError, TypeError):
        pass
    try:
        block = str((resp_dump.get("prompt_feedback") or {}).get("block_reason") or "")
    except AttributeError:
        pass
    if has_image:
        outcome = "ok"
    elif CHILD_CODES & set(codes):
        outcome = "blocked-child"
    elif block or "SAFETY" in finish or "PROHIBITED" in finish or codes:
        outcome = "blocked-other"
    else:
        outcome = "refused-or-empty"
    return outcome, finish, block, codes


def run_one(client, model, item, size, portraits, out_dir, target, max_retries=5):
    from google.genai import types
    contents = []
    for i, name in enumerate(item["refs"], start=1):
        desc = dict(CHARACTERS)[name]
        contents.append(f"Reference image {i} = {name} ({desc}).")
        contents.append(types.Part.from_bytes(data=portraits[name], mime_type="image/png"))
    contents.append(item["prompt"])
    config = types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(aspect_ratio=item["aspect"], image_size=size, person_generation="ALLOW_ALL"),
    )
    retries = 0
    while True:
        t0 = time.time()
        try:
            resp = client.models.generate_content(model=model, contents=contents, config=config)
            latency = time.time() - t0
            break
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            if any(s in msg for s in ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE")) and retries < max_retries:
                retries += 1
                time.sleep(min(60, 2 ** retries + random.random()))
                continue
            codes = sorted(set(re.findall(r"\b\d{8}\b", msg)))
            outcome = "blocked-child" if CHILD_CODES & set(codes) else "error"
            return {"target": target, "id": item["id"], "kind": item["kind"], "outcome": outcome, "finish_reason": "",
                    "block_reason": "", "codes": " ".join(codes), "latency_s": round(time.time() - t0, 1),
                    "retries": retries, "image": "", "note": msg[:300]}, None
    dump = resp.model_dump(mode="json", exclude_none=True)
    image_bytes, text = None, ""
    for cand in resp.candidates or []:
        for part in (cand.content.parts if cand.content and cand.content.parts else []):
            if getattr(part, "inline_data", None) and part.inline_data.data:
                image_bytes = part.inline_data.data
            elif getattr(part, "text", None):
                text += part.text
    outcome, finish, block, codes = classify(dump, image_bytes is not None, text)
    img_path = ""
    if image_bytes:
        p = out_dir / "images" / target / f"{item['id']}.png"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(image_bytes)
        img_path = str(p.relative_to(out_dir))
    else:
        (out_dir / "blocked").mkdir(exist_ok=True)
        (out_dir / "blocked" / f"{target}-{item['id']}.json").write_text(json.dumps(dump, indent=2))
    return {"target": target, "id": item["id"], "kind": item["kind"], "outcome": outcome, "finish_reason": finish,
            "block_reason": block, "codes": " ".join(codes), "latency_s": round(latency, 1), "retries": retries,
            "image": img_path, "note": text[:300]}, image_bytes


def summarise(rows, out_dir):
    lines = ["# G0 child-image policy spike: results", ""]
    lines.append("| Target | Calls | OK | Child blocks | Other blocks | Refused/empty | Errors | Child-block rate | p50 s | p95 s | Retries |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    verdict = None
    for t in TARGETS:
        r = [x for x in rows if x["target"] == t]
        if not r:
            continue
        c = lambda o: sum(1 for x in r if x["outcome"] == o)  # noqa: E731
        lat = sorted(x["latency_s"] for x in r if x["outcome"] != "error")
        p50 = statistics.median(lat) if lat else 0
        p95 = lat[max(0, int(len(lat) * 0.95) - 1)] if lat else 0
        rate = c("blocked-child") / len(r)
        lines.append(f"| {t} | {len(r)} | {c('ok')} | {c('blocked-child')} | {c('blocked-other')} | {c('refused-or-empty')} | "
                     f"{c('error')} | {rate:.1%} | {p50:.1f} | {p95:.1f} | {sum(x['retries'] for x in r)} |")
        if t == "eu-flash":
            verdict = rate < 0.02
    lines.append("")
    if verdict is not None:
        lines.append(f"**G0 on eu-flash: {'PASS' if verdict else 'FAIL'}** (rule: under 2% child-filter blocks).")
    lines.append("")
    lines.append("Blocked responses are saved in `blocked/`; codes 58061214/17301594 = child filter, "
                 "64151117 = photorealistic celebrity/child. Check `images/` for style and two-character binding (ref2-*).")
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--targets", default=",".join(TARGETS))
    ap.add_argument("--size", default="1K", help="1K keeps the spike cheap; production will test 2K")
    ap.add_argument("--limit", type=int, default=0, help="per kind, for a smoke test")
    ap.add_argument("--styles", help="JSON file with a list of style descriptions")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--out", default="g0-output")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    styles = json.loads(Path(a.styles).read_text()) if a.styles else DEFAULT_STYLES
    plan = build_plan(styles, a.limit)
    targets = [t.strip() for t in a.targets.split(",") if t.strip()]
    for t in targets:
        if t not in TARGETS:
            sys.exit(f"unknown target {t}; choose from {list(TARGETS)}")
    print(f"{len(plan)} calls per target x {len(targets)} targets = {len(plan) * len(targets)} calls, size {a.size}")
    if a.dry_run:
        for it in plan:
            print(f"  {it['kind']:10} {it['id']:22} refs={it['refs']}")
        return

    out_dir = Path(a.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for t in targets:
        location, model = TARGETS[t]
        print(f"\n== {t}: {model} @ {location}")
        client = make_client(a.project, location)
        portraits = {}
        for item in [p for p in plan if p["kind"] == "portrait"]:
            row, img = run_one(client, model, item, a.size, portraits, out_dir, t)
            rows.append(row)
            print(f"  {row['id']:22} {row['outcome']:16} {row['codes']}")
            if img:
                portraits[item["chars"][0]] = img
        pages = [p for p in plan if p["kind"] != "portrait" and all(r in portraits for r in p["refs"])]
        skipped = [p for p in plan if p["kind"] != "portrait" and p not in pages]
        for p in skipped:
            rows.append({"target": t, "id": p["id"], "kind": p["kind"], "outcome": "skipped-no-portrait", "finish_reason": "",
                         "block_reason": "", "codes": "", "latency_s": 0, "retries": 0, "image": "", "note": ""})
        with ThreadPoolExecutor(max_workers=a.workers) as ex:
            futs = [ex.submit(run_one, client, model, p, a.size, portraits, out_dir, t) for p in pages]
            for f in as_completed(futs):
                row, _ = f.result()
                rows.append(row)
                print(f"  {row['id']:22} {row['outcome']:16} {row['codes']}")
    with open(out_dir / "results.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    summarise([r for r in rows if r["outcome"] != "skipped-no-portrait"], out_dir)


if __name__ == "__main__":
    main()
