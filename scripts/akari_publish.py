#!/usr/bin/env python3
"""Publish the next Akari daily story onto the static GitHub Pages site.

This script is website-only. It never posts to X and never marks X as published.

The public repository must not contain an unpublished story. Keep the inbox
outside the repo until that entry's release time, then run this script. It
writes one entry per invocation, in numerical order, and only at or after
07:00 America/Los_Angeles on that entry's release day.

Entries 1 and 2 have built-in floors:

  Entry 1  2026-11-06 07:00 America/Los_Angeles
  Entry 2  2026-11-07 07:00 America/Los_Angeles

Entry 3 and later require ``release_not_before`` in the private manifest.
A date-only value means 07:00 America/Los_Angeles that morning. An earlier
clock time is raised to 07:00 that Pacific morning. A later time is kept.

After an entry is published, the next one also waits until the following
Pacific calendar date. One run never releases two numbers. If the next image
or text is missing, the script stops without inventing a story or skipping
ahead.

Usage:
  python3 scripts/akari_publish.py --inbox /path/to/private/inbox
  python3 scripts/akari_publish.py --inbox /path/to/private/inbox --apply --expect 1
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

SITE_ORIGIN = "https://hellabayarea.github.io/portfolio"
PACIFIC = ZoneInfo("America/Los_Angeles")
STORY_ROOT = Path("akari/stories")
MARKER_START = "<!-- akari-stories:start -->"
MARKER_END = "<!-- akari-stories:end -->"
BUILTIN_NOT_BEFORE = {
    1: "2026-11-06T07:00:00-08:00",
    2: "2026-11-07T07:00:00-08:00",
}
FORBIDDEN_VOICE = ("kyle", "ramirez", "カイル", "ラミレス", "明里")
DATE_PATTERNS = (
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
    re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b"),
    re.compile(
        r"\b(?:January|February|March|April|May|June|July|August|September|"
        r"October|November|December)\b"
    ),
)
FILENAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,80}\.jpe?g$")


class PublishError(ValueError):
    """A story failed validation or would break the sequence."""


def empty_catalog() -> dict:
    return {
        "schema": 1,
        "character": "Akari",
        "numbering": "sequential_entry_numbers",
        "site_origin": SITE_ORIGIN,
        "timezone": "America/Los_Angeles",
        "release_hour_local": 7,
        "x_destination": "manual-not-published-by-this-project",
        "entries": [],
    }


def catalog_path(dest: Path) -> Path:
    return dest / STORY_ROOT / "catalog.json"


def dumps(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(data)
    os.replace(temporary, path)


def parse_now(value: str | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise PublishError("--now must include a timezone offset")
    return parsed


def parse_not_before(value: str) -> datetime:
    raw = value.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
        year, month, day = (int(part) for part in raw.split("-"))
        local = datetime(year, month, day, 7, 0, tzinfo=PACIFIC)
    else:
        local = datetime.fromisoformat(raw)
        if local.tzinfo is None:
            raise PublishError("release_not_before must include a timezone offset or be a date")
        local = local.astimezone(PACIFIC)
    seven = local.replace(hour=7, minute=0, second=0, microsecond=0)
    if local < seven:
        return seven
    return local


def effective_not_before(number: int, raw: str | None) -> datetime:
    floors = [parse_not_before(BUILTIN_NOT_BEFORE[number])] if number in BUILTIN_NOT_BEFORE else []
    if raw:
        floors.append(parse_not_before(raw))
    elif number not in BUILTIN_NOT_BEFORE:
        raise PublishError(
            f"entry {number} needs release_not_before in the private manifest "
            "(a calendar date means 07:00 America/Los_Angeles)"
        )
    return max(floors)


def pacific_date(moment: datetime) -> str:
    return moment.astimezone(PACIFIC).date().isoformat()


ENTRY_ONE_CLOSING = "I am Akari, and I'm only beginning."
ENTRY_ONE_SIGNATURE = f"{ENTRY_ONE_CLOSING} 🌸💙"


def apply_entry_signature(number: int, paragraphs: list[str]) -> list[str]:
    """Append the requested Entry 1 signature without changing any other line."""
    if number != 1 or not paragraphs:
        return paragraphs
    last = paragraphs[-1].rstrip()
    if last == ENTRY_ONE_SIGNATURE:
        updated = ENTRY_ONE_SIGNATURE
    elif last == ENTRY_ONE_CLOSING:
        updated = ENTRY_ONE_SIGNATURE
    else:
        return paragraphs
    return [*paragraphs[:-1], updated]


def canonical_markdown(number: int, paragraphs: list[str]) -> str:
    return f"# Entry {number}\n\n" + "\n\n".join(paragraphs) + "\n"


def assert_public_voice(text: str, label: str) -> None:
    lowered = text.casefold()
    for word in FORBIDDEN_VOICE:
        if word.casefold() in lowered:
            raise PublishError(
                f"{label} must call the creator 'my creator' and spell Akari in English letters only"
            )
    for pattern in DATE_PATTERNS:
        if pattern.search(text):
            raise PublishError(f"{label} must not include a calendar date")


def parse_entry_markdown(text: str, number: int) -> list[str]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if normalized.startswith("\ufeff"):
        raise PublishError(f"entry {number} text must not include a BOM")
    expected = f"# Entry {number}\n\n"
    if not normalized.startswith(expected):
        raise PublishError(f'entry {number} must start with "# Entry {number}" and a blank line')
    body = normalized[len(expected) :]
    if body.endswith("\n"):
        body = body[:-1]
    paragraphs = []
    for part in body.split("\n\n"):
        paragraph = part.strip()
        if not paragraph:
            continue
        if paragraph.startswith("#"):
            raise PublishError(f"entry {number} can only have the entry heading")
        paragraphs.append(paragraph)
    if not paragraphs:
        raise PublishError(f"entry {number} has no story text")
    return paragraphs


def jpeg_size(data: bytes) -> tuple[int, int]:
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        raise PublishError("image is not a JPEG")
    index = 2
    while index + 1 < len(data):
        if data[index] != 0xFF:
            raise PublishError("image is not a readable JPEG")
        while index < len(data) and data[index] == 0xFF:
            index += 1
        if index >= len(data):
            break
        marker = data[index]
        index += 1
        if marker in (0xD8, 0xD9):
            continue
        if marker == 0xDA or index + 2 > len(data):
            break
        length = int.from_bytes(data[index : index + 2], "big")
        if length < 2 or index + length > len(data):
            break
        if marker in (0xC0, 0xC1, 0xC2, 0xC3):
            height = int.from_bytes(data[index + 3 : index + 5], "big")
            width = int.from_bytes(data[index + 5 : index + 7], "big")
            if width < 1 or height < 1:
                raise PublishError("image has an empty JPEG frame")
            return width, height
        index += length
    raise PublishError("image is not a readable JPEG")


def load_catalog(dest: Path) -> dict:
    path = catalog_path(dest)
    if not path.exists():
        return empty_catalog()
    catalog = json.loads(path.read_text(encoding="utf-8"))
    if catalog.get("schema") != 1 or catalog.get("character") != "Akari":
        raise PublishError("catalog.json has an unexpected schema")
    if catalog.get("x_destination") != "manual-not-published-by-this-project":
        raise PublishError("catalog.json must leave X unmanaged by this project")
    entries = catalog.get("entries")
    if not isinstance(entries, list):
        raise PublishError("catalog.json entries must be a list")
    for index, entry in enumerate(entries, start=1):
        if entry.get("number") != index or entry.get("id") != f"entry_{index:02d}":
            raise PublishError("catalog entries must stay sequential, with no gaps")
        website = entry.get("publish", {}).get("website", {})
        if website.get("status") != "published":
            raise PublishError(f"catalog entry {index} is not a finished website publication")
        if "x" in entry.get("publish", {}):
            raise PublishError("catalog must not record an X publication claim")
        if not entry.get("paragraphs") or not entry.get("image", {}).get("sha256"):
            raise PublishError(f"catalog entry {index} is missing text or image identity")
    return catalog


def load_manifest(inbox: Path) -> list[dict]:
    path = inbox / "manifest.json"
    if not path.exists():
        return []
    manifest = json.loads(path.read_text(encoding="utf-8"))
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        raise PublishError("manifest entries must be a list")
    seen: set[int] = set()
    loaded = []
    for entry in entries:
        number = entry.get("number")
        if not isinstance(number, int) or number < 1:
            raise PublishError("each entry number must be a positive integer")
        if number in seen:
            raise PublishError(f"duplicate entry number {number}")
        seen.add(number)
        if entry.get("id") != f"entry_{number:02d}":
            raise PublishError(f"entry {number} id must be entry_{number:02d}")
        if entry.get("title_heading") != f"Entry {number}":
            raise PublishError(f"entry {number} title_heading must be 'Entry {number}'")
        loaded.append(entry)
    return loaded


def read_entry_files(inbox: Path, entry: dict) -> dict:
    number = entry["number"]
    text_name = entry.get("text_file")
    if not isinstance(text_name, str) or Path(text_name).name != text_name:
        raise PublishError(f"entry {number} text_file must be a file name in the inbox")
    text_path = inbox / text_name
    if not text_path.is_file():
        raise PublishError(f"entry {number} text file is missing")
    paragraphs = parse_entry_markdown(text_path.read_text(encoding="utf-8"), number)
    if isinstance(entry.get("text"), str):
        mirrored = parse_entry_markdown(entry["text"], number)
        if mirrored != paragraphs:
            raise PublishError(f"entry {number} text file and manifest text do not match")
    image = entry.get("image") or {}
    filename = image.get("filename")
    relative = image.get("path")
    alt = image.get("suggested_alt")
    if not isinstance(filename, str) or not FILENAME_RE.fullmatch(filename):
        raise PublishError(f"entry {number} needs a safe JPEG filename")
    if not isinstance(relative, str) or relative.startswith("/") or ".." in Path(relative).parts:
        raise PublishError(f"entry {number} image path must be a relative inbox path")
    if Path(relative).name != filename:
        raise PublishError(f"entry {number} image filename and path do not match")
    if not isinstance(alt, str) or not alt.strip():
        raise PublishError(f"entry {number} needs suggested_alt text")
    image_path = (inbox / relative).resolve()
    inbox_root = inbox.resolve()
    if inbox_root not in image_path.parents or not image_path.is_file():
        raise PublishError(f"entry {number} image is missing")
    image_bytes = image_path.read_bytes()
    width, height = jpeg_size(image_bytes)
    absolute = entry.get("image", {}).get("absolute_path")
    published_path = f"akari/stories/images/{filename}"
    rewritten = []
    for paragraph in paragraphs:
        updated = paragraph
        if isinstance(absolute, str) and absolute:
            updated = updated.replace(absolute, published_path)
        updated = re.sub(
            rf"(?<!akari/stories/){re.escape(relative)}",
            published_path,
            updated,
        )
        if "/workspace/" in updated or "absolute_path" in updated:
            raise PublishError(f"entry {number} still contains a private path")
        rewritten.append(updated)
    for paragraph in rewritten:
        assert_public_voice(paragraph, f"entry {number}")
    assert_public_voice(alt.strip(), f"entry {number} alt text")
    rewritten = apply_entry_signature(number, rewritten)
    canonical = canonical_markdown(number, rewritten)
    return {
        "number": number,
        "id": f"entry_{number:02d}",
        "title_heading": f"Entry {number}",
        "paragraphs": rewritten,
        "text_sha256": sha256_bytes(canonical.encode("utf-8")),
        "filename": filename,
        "alt": " ".join(alt.split()),
        "image_bytes": image_bytes,
        "image_sha256": sha256_bytes(image_bytes),
        "width": width,
        "height": height,
        "release_not_before": entry.get("release_not_before"),
    }


def fingerprint(stored: dict) -> tuple[str, str]:
    return stored["text_sha256"], stored["image"]["sha256"]


def esc_text(value: str) -> str:
    return html.escape(value, quote=False).replace("\n", "<br>\n")


def esc_attr(value: str) -> str:
    return html.escape(value, quote=True)


def summarize(paragraph: str, limit: int = 180) -> str:
    compact = " ".join(paragraph.split())
    if len(compact) <= limit:
        return compact
    clipped = compact[:limit].rsplit(" ", 1)[0].rstrip(".,;:")
    return f"{clipped}…"


def page_shell(title: str, description: str, canonical: str, image: str, image_alt: str, depth: int, body: str) -> str:
    home = "../" * depth + "index.html"
    archive = "../" * (depth - 2) if depth > 2 else "./"
    css = """
:root{--bg:#07080c;--card:#12151e;--line:#222736;--text:#eef0f6;--muted:#9aa1b4;--cyan:#4cc9f0}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font-family:Inter,"Noto Sans JP",system-ui,-apple-system,Segoe UI,sans-serif;line-height:1.6;min-height:100vh;display:flex;flex-direction:column}
a{color:inherit}
img{max-width:100%;height:auto;display:block}
.skip{position:absolute;left:-999px;top:8px}
.skip:focus{left:8px;background:#fff;color:#000;padding:8px 12px;z-index:5}
.top{position:sticky;top:0;z-index:2;background:#07080ce6;backdrop-filter:blur(10px);border-bottom:1px solid #ffffff14}
.top .bar{width:min(1100px,92vw);margin:0 auto;min-height:60px;display:flex;align-items:center;justify-content:space-between;gap:16px}
.logo{font-family:"Bebas Neue",Impact,sans-serif;letter-spacing:2px;font-size:26px;text-decoration:none}
.top nav{display:flex;gap:18px}
.top nav a{color:var(--muted);text-decoration:none;font-size:14px;font-weight:600}
.top nav a:hover,.top nav a:focus-visible{color:#fff}
main{width:min(1100px,92vw);margin:0 auto;padding:32px 0 72px;flex:1}
.eyebrow{letter-spacing:3px;text-transform:uppercase;color:var(--cyan);font-size:12px;margin:0}
h1{font-family:"Bebas Neue",Impact,sans-serif;font-weight:400;font-size:clamp(56px,9vw,84px);line-height:.9;margin:8px 0 18px;letter-spacing:1px}
.lead,.empty{color:#d5d8e4;font-size:18px;max-width:62ch}
.archive{list-style:none;padding:0;margin:28px 0 0;display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
.archive a{display:flex;flex-direction:column;gap:10px;min-height:44px;text-decoration:none;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:10px}
.archive a:hover,.archive a:focus-visible{border-color:var(--cyan);outline:none}
.archive img,.story img{width:100%;aspect-ratio:4/3;object-fit:contain;background:#07080c;border-radius:12px}
.archive span,.story h1{font-family:"Bebas Neue",Impact,sans-serif}
.archive span{font-size:28px;letter-spacing:1px}
.story{width:min(760px,100%);margin:0 auto}
.story figure{margin:0}
.prose p{font-size:18px;line-height:1.75;color:#e6e8f0}
.download,.pager,.jump{margin-top:22px}
.download a,.pager a,.jump a,.intro a{display:inline-flex;align-items:center;min-height:44px;padding:10px 14px;border-radius:12px;border:1px solid var(--line);text-decoration:none;font-weight:600}
.download a,.intro a{background:#4cc9f014;border-color:#4cc9f055}
.pager{display:flex;flex-wrap:wrap;gap:10px}
.pager .next{margin-left:auto}
.jump ol{list-style:none;display:flex;flex-wrap:wrap;gap:8px;padding:0;margin:8px 0 0}
.jump a[aria-current="page"]{border-color:var(--cyan);color:#fff}
footer{border-top:1px solid #ffffff14;color:var(--muted);text-align:center;padding:28px 16px 40px}
a:focus-visible{outline:2px solid var(--cyan);outline-offset:3px}
@media (max-width:720px){main{padding-top:22px}.pager .next{margin-left:0}.top nav{gap:12px}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
""".strip()
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc_attr(title)}</title>
<meta name="description" content="{esc_attr(description)}">
<link rel="canonical" href="{esc_attr(canonical)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Akari">
<meta property="og:title" content="{esc_attr(title)}">
<meta property="og:description" content="{esc_attr(description)}">
<meta property="og:url" content="{esc_attr(canonical)}">
<meta property="og:image" content="{esc_attr(image)}">
<meta property="og:image:alt" content="{esc_attr(image_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc_attr(title)}">
<meta name="twitter:description" content="{esc_attr(description)}">
<meta name="twitter:image" content="{esc_attr(image)}">
<meta name="theme-color" content="#07080c">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&amp;family=Inter:wght@400;600;700&amp;display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="top"><div class="bar">
 <a class="logo" href="{esc_attr(home)}#akari">Portfolio</a>
 <nav aria-label="Akari">
  <a href="{esc_attr(home)}#akari">Akari</a>
  <a href="{esc_attr(archive)}">Stories</a>
 </nav>
</div></header>
<main id="content">
{body}
</main>
<footer>Akari daily stories. One story and one original image at a time.</footer>
</body>
</html>
"""


def render_archive(entries: list[dict]) -> str:
    if entries:
        description = f"Akari's journal, from Entry 1 through Entry {entries[-1]['number']}."
        image = SITE_ORIGIN + "/" + entries[-1]["image"]["path"]
        image_alt = entries[-1]["image"]["alt"]
        items = []
        for entry in entries:
            number = entry["number"]
            items.append(
                "  <li><a href=\"{n}/\">\n"
                "   <img src=\"images/{file}\" alt=\"{alt}\" width=\"{w}\" height=\"{h}\">\n"
                "   <span>Entry {n}</span>\n"
                "  </a></li>".format(
                    n=number,
                    file=esc_attr(entry["image"]["filename"]),
                    alt=esc_attr(entry["image"]["alt"]),
                    w=entry["image"]["width"],
                    h=entry["image"]["height"],
                )
            )
        body = (
            "<h1>Akari</h1>\n"
            f"<p class=\"lead\">{esc_text(description)} Read them in order, starting with Entry 1.</p>\n"
            "<ol class=\"archive\">\n" + "\n".join(items) + "\n</ol>"
        )
    else:
        description = (
            "Akari's daily journal. Entries appear here in order, starting with Entry 1. "
            "One story and one original image at a time."
        )
        image = f"{SITE_ORIGIN}/assets/akari/akari-avatar.jpg"
        image_alt = "Akari portrait: long black hair, cherry blossoms, one glowing blue cybernetic eye, headphones"
        body = (
            "<h1>Akari</h1>\n"
            "<p class=\"empty\" role=\"status\">No entries yet.</p>\n"
            "<p class=\"lead\">The journal starts with Entry 1. Each release adds the next story and its original image. Nothing is shown here before that entry is released.</p>"
        )
    return page_shell(
        "Stories · Akari",
        description,
        f"{SITE_ORIGIN}/akari/stories/",
        image,
        image_alt,
        2,
        body,
    )


def render_entry(entries: list[dict], entry: dict) -> str:
    number = entry["number"]
    filename = entry["image"]["filename"]
    paragraphs = "\n".join(f"<p>{esc_text(paragraph)}</p>" for paragraph in entry["paragraphs"])
    pager = ['<nav class="pager" aria-label="Nearby entries">']
    if number > 1:
        pager.append(f'<a class="prev" href="../{number - 1}/" rel="prev">Entry {number - 1}</a>')
    pager.append('<a href="../">All entries</a>')
    if any(item["number"] == number + 1 for item in entries):
        pager.append(f'<a class="next" href="../{number + 1}/" rel="next">Entry {number + 1}</a>')
    pager.append("</nav>")
    jump = ['<nav class="jump" aria-label="Entries from 1"><ol>']
    for item in entries:
        current = ' aria-current="page"' if item["number"] == number else ""
        jump.append(f'<li><a href="../{item["number"]}/"{current}>Entry {item["number"]}</a></li>')
    jump.append("</ol></nav>")
    body = f"""<article class="story">
 <p class="eyebrow">Akari</p>
 <h1>Entry {number}</h1>
 <figure>
  <img src="../images/{esc_attr(filename)}" alt="{esc_attr(entry["image"]["alt"])}" width="{entry["image"]["width"]}" height="{entry["image"]["height"]}">
 </figure>
 <div class="prose">
{paragraphs}
 </div>
 <p class="download"><a href="../images/{esc_attr(filename)}" download="{esc_attr(filename)}">Download original JPEG</a> <span>{entry["image"]["width"]} × {entry["image"]["height"]}</span></p>
 {''.join(pager)}
 {''.join(jump)}
</article>"""
    return page_shell(
        f"Entry {number} · Akari",
        summarize(entry["paragraphs"][0]),
        f"{SITE_ORIGIN}/akari/stories/{number}/",
        f"{SITE_ORIGIN}/akari/stories/images/{filename}",
        entry["image"]["alt"],
        3,
        body,
    )


def home_fragment(entries: list[dict]) -> str:
    if not entries:
        return (
            '<div class="akari-empty">\n'
            " <p>No entries yet.</p>\n"
            " <p>The journal starts with Entry 1. Each release adds the next story and its original image.</p>\n"
            ' <p><a class="btn" href="akari/stories/">Open the journal</a></p>\n'
            "</div>"
        )
    latest = entries[-1]
    number = latest["number"]
    links = ['<a class="btn" href="akari/stories/">All entries</a>']
    if number > 1:
        links.insert(0, '<a class="btn primary" href="akari/stories/1/">Start at Entry 1</a>')
    links.append(f'<a class="btn" href="akari/stories/{number}/">Read Entry {number}</a>')
    return (
        '<div class="akari-latest">\n'
        f' <a href="akari/stories/{number}/"><img src="akari/stories/images/{esc_attr(latest["image"]["filename"])}" alt="{esc_attr(latest["image"]["alt"])}" width="{latest["image"]["width"]}" height="{latest["image"]["height"]}"></a>\n'
        " <div>\n"
        f"  <h4>Entry {number}</h4>\n"
        f"  <p>{esc_text(latest['paragraphs'][0])}</p>\n"
        f'  <div class="cta">{"".join(links)}</div>\n'
        " </div>\n"
        "</div>"
    )


def replace_home_fragment(page: str, fragment: str) -> str:
    if page.count(MARKER_START) != 1 or page.count(MARKER_END) != 1:
        raise PublishError("index.html must contain exactly one akari-stories marker pair")
    start = page.index(MARKER_START) + len(MARKER_START)
    end = page.index(MARKER_END)
    if end < start:
        raise PublishError("akari-stories markers are out of order")
    return page[:start] + "\n" + fragment + "\n" + page[end:]


def assert_pages_are_public_safe(archive_html: str, entries: list[dict], entry_pages: dict[int, str]) -> None:
    pages = [archive_html, home_fragment(entries), *entry_pages.values()]
    forbidden_markup = ("<form", "<input", "<textarea", "<button", "<script")
    for entry in entries:
        page = entry_pages[entry["number"]]
        if entry["published_pacific_date"] in page or entry["published_pacific_date"] in archive_html:
            raise PublishError("refusing to show a release date on the website")
    for page in pages:
        lowered = page.casefold()
        for snippet in forbidden_markup:
            if snippet in lowered:
                raise PublishError("story pages must not collect visitor input or run scripts")
        for word in ("kyle", "ramirez", "明里"):
            if word in lowered:
                raise PublishError("story pages must not name the creator or use a non-Latin spelling of Akari")


def public_entry(prepared: dict, published_on: str) -> dict:
    number = prepared["number"]
    filename = prepared["filename"]
    return {
        "id": prepared["id"],
        "number": number,
        "title_heading": prepared["title_heading"],
        "paragraphs": prepared["paragraphs"],
        "text_sha256": prepared["text_sha256"],
        "published_pacific_date": published_on,
        "image": {
            "filename": filename,
            "path": f"akari/stories/images/{filename}",
            "bytes": len(prepared["image_bytes"]),
            "sha256": prepared["image_sha256"],
            "width": prepared["width"],
            "height": prepared["height"],
            "alt": prepared["alt"],
        },
        "publish": {
            "website": {
                "status": "published",
                "path": f"akari/stories/{number}/index.html",
                "url": f"{SITE_ORIGIN}/akari/stories/{number}/",
            }
        },
    }


def result(status: str, catalog: dict, **extra) -> dict:
    numbers = [entry["number"] for entry in catalog["entries"]]
    payload = {
        "status": status,
        "published_through": numbers[-1] if numbers else 0,
        "next_number": (numbers[-1] + 1) if numbers else 1,
        "x": "not-managed",
    }
    payload.update(extra)
    return payload


def publish(inbox: Path, dest: Path, now: datetime, apply: bool) -> dict:
    if now.tzinfo is None:
        raise PublishError("now must include a timezone")
    catalog = load_catalog(dest)
    manifest_entries = load_manifest(inbox)
    if not manifest_entries:
        return result("idle", catalog, reason="inbox-empty")

    prepared_by_number = {item["number"]: item for item in manifest_entries}
    for entry in catalog["entries"]:
        incoming = prepared_by_number.get(entry["number"])
        if incoming is None:
            continue
        checked = read_entry_files(inbox, incoming)
        if (checked["text_sha256"], checked["image_sha256"]) != fingerprint(entry):
            raise PublishError(
                f"entry {entry['number']} is already published with different text or image"
            )

    next_number = len(catalog["entries"]) + 1
    raw_candidate = prepared_by_number.get(next_number)
    if raw_candidate is None:
        if any(number > next_number for number in prepared_by_number):
            raise PublishError(f"refusing to skip; entry {next_number} is not in the inbox")
        return result("idle", catalog, reason="next-entry-absent")

    candidate = read_entry_files(inbox, raw_candidate)
    for number in sorted(prepared_by_number):
        if number > next_number:
            read_entry_files(inbox, prepared_by_number[number])

    not_before = effective_not_before(next_number, candidate.get("release_not_before"))
    if now < not_before:
        return result(
            "waiting",
            catalog,
            reason="before-release",
            number=next_number,
            not_before=not_before.astimezone(PACIFIC).isoformat(),
        )
    if catalog["entries"]:
        previous_day = catalog["entries"][-1]["published_pacific_date"]
        if pacific_date(now) <= previous_day:
            return result(
                "waiting",
                catalog,
                reason="same-pacific-day",
                number=next_number,
            )

    for existing in catalog["entries"]:
        if existing["image"]["filename"] == candidate["filename"]:
            raise PublishError("image filename already used by an earlier entry")
    published = public_entry(candidate, pacific_date(now))
    updated = dict(catalog)
    updated["entries"] = [*catalog["entries"], published]
    archive_html = render_archive(updated["entries"])
    entry_pages = {
        item["number"]: render_entry(updated["entries"], item) for item in updated["entries"]
    }
    assert_pages_are_public_safe(archive_html, updated["entries"], entry_pages)
    index_path = dest / "index.html"
    new_index = None
    if index_path.exists():
        new_index = replace_home_fragment(
            index_path.read_text(encoding="utf-8"),
            home_fragment(updated["entries"]),
        )
    payload = result(
        "ready" if not apply else "published",
        updated,
        number=next_number,
        path=published["publish"]["website"]["path"],
        url=published["publish"]["website"]["url"],
        image_sha256=candidate["image_sha256"],
        text_sha256=candidate["text_sha256"],
    )
    if not apply:
        return payload

    image_path = dest / published["image"]["path"]
    if image_path.exists() and sha256_bytes(image_path.read_bytes()) != candidate["image_sha256"]:
        raise PublishError(f"refusing to overwrite a different file at {published['image']['path']}")
    atomic_write(image_path, candidate["image_bytes"])
    if sha256_bytes(image_path.read_bytes()) != candidate["image_sha256"]:
        raise PublishError("written JPEG does not match the original bytes")
    for item in updated["entries"]:
        atomic_write(
            dest / item["publish"]["website"]["path"],
            entry_pages[item["number"]].encode("utf-8"),
        )
    atomic_write(dest / STORY_ROOT / "index.html", archive_html.encode("utf-8"))
    if new_index is not None:
        atomic_write(index_path, new_index.encode("utf-8"))
    atomic_write(catalog_path(dest), dumps(updated).encode("utf-8"))
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Publish the next Akari website story.")
    parser.add_argument("--inbox", required=True, type=Path)
    parser.add_argument("--dest", type=Path, default=Path("."))
    parser.add_argument("--now", help="Timezone-aware ISO time. Defaults to the current time.")
    parser.add_argument("--apply", action="store_true", help="Write the entry. Omit for a dry run.")
    parser.add_argument("--expect", type=int, help="Exit 1 unless this entry number is released or already current.")
    args = parser.parse_args(argv)
    try:
        payload = publish(args.inbox, args.dest, parse_now(args.now), args.apply)
    except (PublishError, json.JSONDecodeError, OSError) as exc:
        print(dumps({"status": "error", "message": str(exc)}))
        return 1
    print(dumps(payload))
    if args.expect is not None:
        numbers = []
        catalog = load_catalog(args.dest) if args.apply else None
        if args.apply and catalog is not None:
            numbers = [entry["number"] for entry in catalog["entries"]]
        expected_ready = payload.get("number") == args.expect and payload["status"] in {
            "published",
            "ready",
            "noop",
        }
        if args.expect not in numbers and not expected_ready:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
