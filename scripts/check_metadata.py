#!/usr/bin/env python3
"""Validate that slide PDFs and metadata/events.yml stay in sync.

Checks, for the whole repository:
  1. Every PDF under slides/ is referenced by an entry in metadata/events.yml.
  2. Every entry's `pdf:` path points to a file that actually exists.
  3. Every entry has the required fields filled in (no leftover placeholders).

Exit code is 0 when everything is consistent, 1 otherwise. Run it locally
with `python3 scripts/check_metadata.py`; CI runs the same command.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
EVENTS_FILE = REPO_ROOT / "metadata" / "events.yml"
SLIDES_DIR = REPO_ROOT / "slides"

REQUIRED_FIELDS = ("year", "date", "venue", "venue_name", "title", "speakers", "pdf")
# Placeholder values copied from templates/metadata-template.yml that must be
# replaced before an entry is considered complete.
PLACEHOLDERS = {
    "Firstname Lastname",
    "Talk Title",
    "Venue Name",
    "venue-key",
    "City, Country",
}


def load_entries() -> list[dict]:
    if not EVENTS_FILE.exists():
        sys.exit(f"error: {EVENTS_FILE.relative_to(REPO_ROOT)} not found")
    data = yaml.safe_load(EVENTS_FILE.read_text()) or []
    if not isinstance(data, list):
        sys.exit("error: metadata/events.yml must be a list of entries")
    return data


def main() -> int:
    entries = load_entries()
    errors: list[str] = []

    # Map declared pdf paths (normalized, repo-relative) -> entry index.
    declared: dict[str, int] = {}
    for i, entry in enumerate(entries):
        label = entry.get("title") or f"entry #{i + 1}"

        for field in REQUIRED_FIELDS:
            value = entry.get(field)
            if value in (None, "", []):
                errors.append(f"[{label}] missing required field: {field}")
            elif isinstance(value, str) and value in PLACEHOLDERS:
                errors.append(f"[{label}] field '{field}' still has placeholder value: {value!r}")

        speakers = entry.get("speakers") or []
        if any(s in PLACEHOLDERS for s in speakers):
            errors.append(f"[{label}] speakers still contains a placeholder name")

        pdf = entry.get("pdf")
        if not pdf:
            continue
        pdf_path = (REPO_ROOT / pdf).resolve()
        rel = pdf
        if not pdf.startswith("slides/"):
            errors.append(f"[{label}] pdf path must live under slides/: {pdf}")
        if not pdf_path.exists():
            errors.append(f"[{label}] pdf file does not exist: {pdf}")
        elif pdf_path.suffix.lower() != ".pdf":
            errors.append(f"[{label}] pdf field does not point to a .pdf file: {pdf}")
        declared[rel] = i

    # Every PDF on disk must be declared in the metadata.
    if SLIDES_DIR.exists():
        for pdf_file in sorted(SLIDES_DIR.rglob("*.pdf")):
            rel = pdf_file.relative_to(REPO_ROOT).as_posix()
            if rel not in declared:
                errors.append(f"[orphan] {rel} has no entry in metadata/events.yml")

    if errors:
        print(f"Metadata validation failed with {len(errors)} problem(s):\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        print(
            "\nFix metadata/events.yml (see templates/metadata-template.yml) "
            "so every slide PDF has a complete, matching entry.",
            file=sys.stderr,
        )
        return 1

    print(f"OK: {len(entries)} metadata entr(y/ies) consistent with slides/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
