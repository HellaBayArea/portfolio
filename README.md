# Kyle's AI Art & Music Portfolio

A portfolio of my AI art, music (Suno), and short videos.

- X: https://x.com/HellaBayArea
- TikTok: https://www.tiktok.com/@hellabayarea88
- Suno: https://suno.com/@detnorske

Static site served with GitHub Pages (`index.html` + `assets/`).

## Akari daily stories

The journal lives at [hellabayarea.github.io/portfolio/akari/stories/](https://hellabayarea.github.io/portfolio/akari/stories/). Entry N is `akari/stories/N/`. The homepage section is `#akari`.

Stories are website-only. This repo does not post to X. Pages do not collect comments or other visitor input. Entry numbers are visible; calendar dates are not.

`akari/stories/catalog.json` starts empty. Do not commit an unpublished story, image, or manifest. This repository is public, so a commit is public immediately. Keep future text and JPEGs outside the repo until that entry's release time.

Release floors, America/Los_Angeles, one entry per run:

- Entry 1: 2026-11-06 06:42, the owner's "Publish now" authorization. Later entries are not included.
- Entry 2: 2026-11-07 07:00
- Entry 3 and later: `release_not_before` in the private manifest. A date means 07:00 that Pacific morning. Earlier times are raised to 07:00. The next entry also waits until the Pacific date after the previous entry was published.

Import folder (private):

```json
{
  "character": "Akari",
  "numbering": "sequential_entry_numbers",
  "entries": [
    {
      "id": "entry_03",
      "number": 3,
      "title_heading": "Entry 3",
      "text_file": "entry_03.md",
      "release_not_before": "2026-11-08",
      "image": {
        "filename": "entry_03_example.jpg",
        "path": "images/entry_03_example.jpg",
        "suggested_alt": "Describe the picture without a date or the creator's name."
      },
      "publish": {
        "x": {"status": "unpublished", "post_id": null, "url": null},
        "website": {"status": "unpublished", "path": null, "url": null}
      }
    }
  ]
}
```

`entry_03.md` starts with `# Entry 3`, a blank line, then the paragraphs. In Akari's own writing the creator is only "my creator", and her name is spelled Akari. The script copies the JPEG bytes unchanged and links that same file as the original download. Entry 1's published last line keeps the approved sentence and appends 🌸💙.

The script does not write future entries. A private drafting routine can prepare Entry 3 or later, but those files stay out of this public repo until that entry's own release, and this workflow does not generate them. The scheduled workflow file is not active on `main` until this branch is merged, and even then it only sees files already committed to the public inbox.

At or after the release time, from a checkout of `main`:

```bash
python3 scripts/akari_publish.py --inbox /absolute/path/to/private/inbox
python3 scripts/akari_publish.py --inbox /absolute/path/to/private/inbox --apply --expect 3
```

The first command is a dry run. `--apply` writes only the next entry: its page, the original JPEG, the archive, the catalog, and the marked block in `index.html`. Review the diff, commit those files, and open a PR. The live site updates when that PR is merged. Merging is manual.

If the inbox has no ready entry, the script stops. It does not invent a story, repeat one, or skip a number. Publishing the same bytes again is a no-op. A different file for an existing number is refused.

`.github/workflows/akari-daily-story.yml` runs at 14:00 and 15:00 UTC so one of those hours is 07:00 Pacific across daylight-saving time. It can only publish a story that is already in the public `akari/inbox/` folder, which is the wrong place for an unreleased draft. GitHub may also start the schedule late. Unattended publishing is blocked until someone supplies the private files at release time and the result reaches `main`.
