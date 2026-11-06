import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import akari_publish as publisher  # noqa: E402

JPEG = bytes([
    0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46, 0x00, 0x01,
    0x01, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0xFF, 0xDB, 0x00, 0x43,
    0x00, 0x08, 0x06, 0x06, 0x07, 0x06, 0x05, 0x08, 0x07, 0x07, 0x07, 0x09,
    0x09, 0x08, 0x0A, 0x0C, 0x14, 0x0D, 0x0C, 0x0B, 0x0B, 0x0C, 0x19, 0x12,
    0x13, 0x0F, 0x14, 0x1D, 0x1A, 0x1F, 0x1E, 0x1D, 0x1A, 0x1C, 0x1C, 0x20,
    0x24, 0x2E, 0x27, 0x20, 0x22, 0x2C, 0x23, 0x1C, 0x1C, 0x28, 0x37, 0x29,
    0x2C, 0x30, 0x31, 0x34, 0x34, 0x34, 0x1F, 0x27, 0x39, 0x3D, 0x38, 0x32,
    0x3C, 0x2E, 0x33, 0x34, 0x32, 0xFF, 0xC0, 0x00, 0x0B, 0x08, 0x00, 0x01,
    0x00, 0x01, 0x01, 0x01, 0x11, 0x00, 0xFF, 0xC4, 0x00, 0x14, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x09, 0xFF, 0xC4, 0x00, 0x14, 0x10, 0x01, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0xFF, 0xDA, 0x00, 0x08, 0x01, 0x01, 0x00, 0x00, 0x3F, 0x00,
    0x54, 0xDF, 0xFF, 0xD9,
])
INDEX = """<!doctype html>
<html><body>
<p>Kyle Ramirez keeps the portfolio byline.</p>
<!-- akari-stories:start -->
<div class="akari-empty">placeholder</div>
<!-- akari-stories:end -->
<p>More Kyle Ramirez text.</p>
</body></html>
"""


def at(value):
    return datetime.fromisoformat(value)


def write_inbox(root, entries):
    payload = {"character": "Akari", "numbering": "sequential_entry_numbers", "entries": []}
    for entry in entries:
        number = entry["number"]
        filename = entry.get("filename", f"entry_{number:02d}.jpg")
        text = entry.get(
            "text",
            f"# Entry {number}\n\nAlpha {number} & beta.\n\nDon't stop.\n",
        )
        (root / f"entry_{number:02d}.md").write_text(text, encoding="utf-8")
        image = root / "images" / filename
        image.parent.mkdir(parents=True, exist_ok=True)
        image.write_bytes(entry.get("image", JPEG))
        item = {
            "id": f"entry_{number:02d}",
            "number": number,
            "title_heading": f"Entry {number}",
            "text_file": f"entry_{number:02d}.md",
            "image": {
                "filename": filename,
                "path": f"images/{filename}",
                "suggested_alt": entry.get("alt", f"Akari illustration {number}"),
            },
            "publish": {
                "x": entry.get("x", {"status": "unpublished", "post_id": None, "url": None}),
                "website": {"status": "unpublished", "path": None, "url": None},
            },
        }
        if "manifest_text" in entry:
            item["text"] = entry["manifest_text"]
        if "absolute_path" in entry:
            item["image"]["absolute_path"] = entry["absolute_path"]
        if "release_not_before" in entry:
            item["release_not_before"] = entry["release_not_before"]
        payload["entries"].append(item)
    (root / "manifest.json").write_text(json.dumps(payload), encoding="utf-8")


class PublishTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.inbox = self.root / "inbox"
        self.dest = self.root / "site"
        self.inbox.mkdir()
        self.dest.mkdir()
        (self.dest / "index.html").write_text(INDEX, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def publish(self, now, apply=True):
        return publisher.publish(self.inbox, self.dest, at(now), apply)

    def test_jpeg_dimensions(self):
        self.assertEqual(publisher.jpeg_size(JPEG), (1, 1))

    def test_scaffold_matches_empty_renderer(self):
        archive = (ROOT / "akari/stories/index.html").read_text(encoding="utf-8")
        catalog = json.loads((ROOT / "akari/stories/catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(archive, publisher.render_archive([]))
        self.assertEqual(catalog, publisher.empty_catalog())
        page = (ROOT / "index.html").read_text(encoding="utf-8")
        start = page.index(publisher.MARKER_START) + len(publisher.MARKER_START)
        end = page.index(publisher.MARKER_END)
        self.assertEqual(page[start:end].strip(), publisher.home_fragment([]).strip())
        self.assertIn("Kyle Ramirez", page)
        self.assertEqual(list((ROOT / "akari/stories/images").glob("*.jpg")), [])
        self.assertEqual(list(ROOT.rglob("entry_*.md")), [])

    def test_before_release_writes_nothing(self):
        write_inbox(self.inbox, [{"number": 1}])
        before = self.snapshot()
        result = self.publish("2026-11-06T06:59:59-08:00")
        self.assertEqual(result["status"], "waiting")
        self.assertEqual(result["reason"], "before-release")
        self.assertEqual(before, self.snapshot())
        self.assertFalse((self.dest / "akari/stories/catalog.json").exists())

    def test_entry_one_signature_appends_once(self):
        closing = publisher.ENTRY_ONE_CLOSING
        signed = publisher.ENTRY_ONE_SIGNATURE
        self.assertEqual(publisher.apply_entry_signature(1, ["Hello.", closing]), ["Hello.", signed])
        self.assertEqual(publisher.apply_entry_signature(1, ["Hello.", signed]), ["Hello.", signed])
        self.assertEqual(publisher.apply_entry_signature(2, ["Hello.", closing]), ["Hello.", closing])
        write_inbox(self.inbox, [{"number": 1, "text": f"# Entry 1\n\nHello from the journal.\n\n{closing}\n"}])
        self.publish("2026-11-06T06:59:00-08:00")
        self.assertFalse((self.dest / "akari/stories/1/index.html").exists())
        self.publish("2026-11-06T07:00:00-08:00")
        page = (self.dest / "akari/stories/1/index.html").read_text(encoding="utf-8")
        self.assertEqual(page.count("🌸💙"), 1)
        self.assertIn(signed, page)
        self.assertNotIn("2026-11-06", page)
        catalog = json.loads((self.dest / "akari/stories/catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["entries"][0]["paragraphs"][-1], signed)
        self.assertEqual((self.dest / "akari/stories/images/entry_01.jpg").read_bytes(), JPEG)

    def test_publishes_entry_one_at_0700_pacific(self):
        write_inbox(self.inbox, [{"number": 1, "manifest_text": "# Entry 1\n\nAlpha 1 & beta.\n\nDon't stop.\n"}])
        result = self.publish("2026-11-06T07:00:00-08:00")
        self.assertEqual(result["status"], "published")
        self.assertEqual(result["url"], "https://hellabayarea.github.io/portfolio/akari/stories/1/")
        page = (self.dest / "akari/stories/1/index.html").read_text(encoding="utf-8")
        image = (self.dest / "akari/stories/images/entry_01.jpg").read_bytes()
        self.assertEqual(image, JPEG)
        self.assertIn("Alpha 1 &amp; beta.", page)
        self.assertIn("Don't stop.", page)
        self.assertIn('rel="canonical" href="https://hellabayarea.github.io/portfolio/akari/stories/1/"', page)
        self.assertIn("https://hellabayarea.github.io/portfolio/akari/stories/images/entry_01.jpg", page)
        self.assertIn('download="entry_01.jpg"', page)
        self.assertNotIn("<form", page.casefold())
        self.assertNotIn("<input", page.casefold())
        self.assertNotIn("<textarea", page.casefold())
        self.assertNotIn("<button", page.casefold())
        self.assertNotIn("2026-11-06", page)
        self.assertNotIn("kyle", page.casefold())
        catalog = json.loads((self.dest / "akari/stories/catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["entries"][0]["publish"]["website"]["status"], "published")
        self.assertNotIn("x", catalog["entries"][0]["publish"])
        self.assertNotIn("x", result["status"])
        home = (self.dest / "index.html").read_text(encoding="utf-8")
        self.assertEqual(home.count("Kyle Ramirez"), 2)
        self.assertIn("Read Entry 1", home)
        self.assertNotIn("placeholder", home)

    def test_utc_equivalent_of_0700_pst(self):
        write_inbox(self.inbox, [{"number": 1}])
        result = self.publish("2026-11-06T15:00:00+00:00")
        self.assertEqual(result["status"], "published")

    def test_builtin_floor_beats_an_earlier_request(self):
        write_inbox(self.inbox, [{"number": 1, "release_not_before": "2026-11-05T07:00:00-08:00"}])
        result = self.publish("2026-11-05T12:00:00-08:00")
        self.assertEqual(result["status"], "waiting")

    def test_dry_run_does_not_write(self):
        write_inbox(self.inbox, [{"number": 1}])
        before = self.snapshot()
        result = self.publish("2026-11-06T07:00:00-08:00", apply=False)
        self.assertEqual(result["status"], "ready")
        self.assertEqual(before, self.snapshot())

    def test_second_run_is_idempotent(self):
        write_inbox(self.inbox, [{"number": 1}])
        self.publish("2026-11-06T07:00:00-08:00")
        first = self.snapshot()
        result = self.publish("2026-11-07T07:00:00-08:00")
        self.assertEqual(result["status"], "idle")
        self.assertEqual(result["reason"], "next-entry-absent")
        self.assertEqual(first, self.snapshot())

    def test_refuses_to_skip_or_invent(self):
        write_inbox(self.inbox, [{"number": 2}])
        with self.assertRaises(publisher.PublishError):
            self.publish("2026-11-08T07:00:00-08:00")
        self.assertFalse((self.dest / "akari/stories/2/index.html").exists())

    def test_one_entry_per_run_even_when_both_are_due(self):
        write_inbox(self.inbox, [{"number": 1}, {"number": 2}])
        result = self.publish("2026-11-08T07:00:00-08:00")
        self.assertEqual(result["number"], 1)
        self.assertTrue((self.dest / "akari/stories/1/index.html").exists())
        self.assertFalse((self.dest / "akari/stories/2/index.html").exists())
        self.assertFalse((self.dest / "akari/stories/images/entry_02.jpg").exists())

    def test_same_pacific_day_holds_the_next_entry(self):
        write_inbox(self.inbox, [{"number": 1}, {"number": 2}])
        first = self.publish("2026-11-07T07:00:00-08:00")
        self.assertEqual(first["number"], 1)
        held = self.publish("2026-11-07T08:00:00-08:00")
        self.assertEqual(held["status"], "waiting")
        self.assertEqual(held["reason"], "same-pacific-day")
        released = self.publish("2026-11-08T07:00:00-08:00")
        self.assertEqual(released["number"], 2)
        first_page = (self.dest / "akari/stories/1/index.html").read_text(encoding="utf-8")
        self.assertIn('href="../2/" rel="next"', first_page)
        self.assertEqual((self.dest / "akari/stories/images/entry_01.jpg").read_bytes(), JPEG)
        catalog = json.loads((self.dest / "akari/stories/catalog.json").read_text(encoding="utf-8"))
        self.assertEqual([entry["number"] for entry in catalog["entries"]], [1, 2])

    def test_changed_bytes_for_an_existing_entry_are_refused(self):
        write_inbox(self.inbox, [{"number": 1}, {"number": 2}])
        self.publish("2026-11-06T07:00:00-08:00")
        write_inbox(self.inbox, [
            {"number": 1, "text": "# Entry 1\n\nDifferent words.\n"},
            {"number": 2},
        ])
        with self.assertRaises(publisher.PublishError):
            self.publish("2026-11-08T07:00:00-08:00")
        catalog = json.loads((self.dest / "akari/stories/catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(len(catalog["entries"]), 1)
        self.assertIn("Alpha 1", catalog["entries"][0]["paragraphs"][0])

    def test_escapes_markup_and_rewrites_private_paths(self):
        absolute = "/workspace/private/entry_01_sun.jpg"
        text = (
            "# Entry 1\n\n"
            "See /workspace/private/entry_01_sun.jpg now.\n\n"
            "Don't <b>stop</b>.\n"
        )
        write_inbox(self.inbox, [{
            "number": 1,
            "filename": "entry_01_sun.jpg",
            "absolute_path": absolute,
            "text": text,
            "manifest_text": text,
        }])
        self.publish("2026-11-06T07:00:00-08:00")
        page = (self.dest / "akari/stories/1/index.html").read_text(encoding="utf-8")
        self.assertIn("See akari/stories/images/entry_01_sun.jpg now.", page)
        self.assertIn("Don't &lt;b&gt;stop&lt;/b&gt;.", page)
        self.assertNotIn("<b>stop</b>", page)
        self.assertNotIn("/workspace/", page)

    def test_rejects_creator_name_bad_image_and_text_mismatch(self):
        write_inbox(self.inbox, [{"number": 1, "text": "# Entry 1\n\nHello Kyle.\n"}])
        with self.assertRaises(publisher.PublishError):
            self.publish("2026-11-06T07:00:00-08:00")
        write_inbox(self.inbox, [{"number": 1, "text": "# Entry 1\n\nHello 明里.\n"}])
        with self.assertRaises(publisher.PublishError):
            self.publish("2026-11-06T07:00:00-08:00")
        write_inbox(self.inbox, [{"number": 1, "text": "# Entry 1\n\nNovember rain.\n"}])
        with self.assertRaises(publisher.PublishError):
            self.publish("2026-11-06T07:00:00-08:00")
        write_inbox(self.inbox, [{"number": 1, "image": b"not-a-jpeg"}])
        with self.assertRaises(publisher.PublishError):
            self.publish("2026-11-06T07:00:00-08:00")
        write_inbox(self.inbox, [{
            "number": 1,
            "manifest_text": "# Entry 1\n\nOther words.\n",
        }])
        with self.assertRaises(publisher.PublishError):
            self.publish("2026-11-06T07:00:00-08:00")
        self.assertFalse((self.dest / "akari/stories/catalog.json").exists())

    def test_entry_three_requires_a_release_floor(self):
        write_inbox(self.inbox, [{"number": 1}])
        self.publish("2026-11-06T07:00:00-08:00")
        write_inbox(self.inbox, [{"number": 2}])
        self.publish("2026-11-07T07:00:00-08:00")
        write_inbox(self.inbox, [{"number": 3}])
        with self.assertRaises(publisher.PublishError):
            self.publish("2026-11-09T07:00:00-08:00")
        write_inbox(self.inbox, [{"number": 3, "release_not_before": "2026-11-08"}])
        early = self.publish("2026-11-08T06:30:00-08:00")
        self.assertEqual(early["status"], "waiting")
        released = self.publish("2026-11-08T07:00:00-08:00")
        self.assertEqual(released["status"], "published")
        self.assertEqual(released["number"], 3)

    def test_inbox_claim_cannot_mark_x_published(self):
        write_inbox(self.inbox, [{
            "number": 1,
            "x": {"status": "published", "post_id": "1", "url": "https://x.com/example/status/1"},
        }])
        self.publish("2026-11-06T07:00:00-08:00")
        catalog = json.loads((self.dest / "akari/stories/catalog.json").read_text(encoding="utf-8"))
        self.assertNotIn("x", catalog["entries"][0]["publish"])
        page = (self.dest / "akari/stories/1/index.html").read_text(encoding="utf-8")
        self.assertNotIn("x.com", page)

    def test_daylight_saving_date_means_0700_local(self):
        moment = publisher.parse_not_before("2027-07-06")
        local = moment.astimezone(publisher.PACIFIC)
        self.assertEqual((local.hour, local.minute), (7, 0))
        self.assertEqual(moment.astimezone(publisher.PACIFIC).utcoffset().total_seconds(), -7 * 3600)

    def test_workflow_is_website_only(self):
        workflow = (ROOT / ".github/workflows/akari-daily-story.yml").read_text(encoding="utf-8")
        self.assertIn('cron: "0 14 * * *"', workflow)
        self.assertIn('cron: "0 15 * * *"', workflow)
        self.assertIn("contents: write", workflow)
        self.assertNotIn("x.com", workflow)
        self.assertNotIn("api.twitter", workflow)
        self.assertNotIn("secrets.", workflow)
        inbox = ROOT / "akari/inbox"
        self.assertFalse((inbox / "manifest.json").exists())
        self.assertEqual(list(inbox.glob("*.jpg")), [])

    def test_cli_expect_and_empty_inbox(self):
        script = ROOT / "scripts/akari_publish.py"
        empty = subprocess.run(
            [sys.executable, str(script), "--inbox", str(self.inbox), "--dest", str(self.dest), "--apply"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(empty.returncode, 0)
        self.assertEqual(json.loads(empty.stdout)["status"], "idle")
        write_inbox(self.inbox, [{"number": 1}])
        early = subprocess.run(
            [
                sys.executable, str(script), "--inbox", str(self.inbox), "--dest", str(self.dest),
                "--apply", "--expect", "1", "--now", "2026-11-05T23:00:00-08:00",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(early.returncode, 1)
        self.assertFalse((self.dest / "akari/stories/1/index.html").exists())

    def test_private_bundle_when_available(self):
        raw = os.environ.get("AKARI_PRIVATE_INBOX")
        if not raw or not (Path(raw) / "manifest.json").exists():
            self.skipTest("AKARI_PRIVATE_INBOX is not set")
        inbox = Path(raw)
        early = publisher.publish(inbox, self.dest, at("2026-11-05T23:30:00-08:00"), True)
        self.assertEqual(early["status"], "waiting")
        self.assertFalse((self.dest / "akari/stories/1/index.html").exists())
        released = publisher.publish(inbox, self.dest, at("2026-11-06T07:00:00-08:00"), True)
        self.assertEqual(released["status"], "published")
        self.assertEqual(released["number"], 1)
        manifest = json.loads((inbox / "manifest.json").read_text(encoding="utf-8"))
        first = next(item for item in manifest["entries"] if item["number"] == 1)
        second_spec = next(item for item in manifest["entries"] if item["number"] == 2)
        source = (inbox / first["text_file"]).read_text(encoding="utf-8")
        paragraphs = publisher.apply_entry_signature(1, publisher.parse_entry_markdown(source, 1))
        page = (self.dest / "akari/stories/1/index.html").read_text(encoding="utf-8")
        for paragraph in paragraphs:
            self.assertIn(publisher.esc_text(paragraph), page)
        self.assertEqual(page.count("🌸💙"), 1)
        image_name = first["image"]["filename"]
        copied = (self.dest / "akari/stories/images" / image_name).read_bytes()
        self.assertEqual(copied, (inbox / first["image"]["path"]).read_bytes())
        self.assertEqual(hashlib.sha256(copied).hexdigest(), released["image_sha256"])
        self.assertFalse((self.dest / "akari/stories/images" / second_spec["image"]["filename"]).exists())
        self.assertNotIn("2026-11-06", page)
        catalog = json.loads((self.dest / "akari/stories/catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["x_destination"], "manual-not-published-by-this-project")
        again = publisher.publish(inbox, self.dest, at("2026-11-06T09:00:00-08:00"), True)
        self.assertEqual(again["status"], "waiting")
        self.assertEqual(again["reason"], "before-release")
        second = publisher.publish(inbox, self.dest, at("2026-11-07T07:00:00-08:00"), True)
        self.assertEqual(second["number"], 2)
        second_page = (self.dest / "akari/stories/2/index.html").read_text(encoding="utf-8")
        self.assertNotIn("🌸💙", second_page)
        self.assertNotIn("2026-11-07", second_page)
        second_image = self.dest / "akari/stories/images" / second_spec["image"]["filename"]
        self.assertEqual(second_image.read_bytes(), (inbox / second_spec["image"]["path"]).read_bytes())
        self.assertEqual((self.dest / "akari/stories/images" / image_name).read_bytes(), copied)

    def snapshot(self):
        hashes = {}
        for path in sorted(self.dest.rglob("*")):
            if path.is_file():
                hashes[str(path.relative_to(self.dest))] = hashlib.sha256(path.read_bytes()).hexdigest()
        return hashes


if __name__ == "__main__":
    unittest.main()
