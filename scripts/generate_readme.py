#!/usr/bin/env python3
"""Generate the README presentation tables from metadata/events.yml.

metadata/events.yml is the single source of truth. The tables under
"## Presentations by year" in README.md are rebuilt from it, grouped by year
(newest first). Everything between the BEGIN/END markers is owned by this
script; the rest of the README is hand-edited.

Usage:
  python3 scripts/generate_readme.py          # rewrite README.md in place
  python3 scripts/generate_readme.py --check   # exit 1 if README is stale (CI)
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
EVENTS_FILE = REPO_ROOT / "metadata" / "events.yml"
README_FILE = REPO_ROOT / "README.md"

BEGIN = "<!-- BEGIN:presentations (auto-generated from metadata/events.yml by scripts/generate_readme.py — do not edit by hand) -->"
END = "<!-- END:presentations -->"


def load_entries() -> list[dict]:
    data = yaml.safe_load(EVENTS_FILE.read_text()) or []
    if not isinstance(data, list):
        sys.exit("error: metadata/events.yml must be a list of entries")
    return data


def build_tables(entries: list[dict]) -> str:
    by_year: dict[int, list[dict]] = {}
    for entry in entries:
        by_year.setdefault(int(entry["year"]), []).append(entry)

    lines: list[str] = []
    for year in sorted(by_year, reverse=True):
        rows = sorted(by_year[year], key=lambda e: str(e.get("date", "")), reverse=True)
        lines.append(f"### {year}")
        lines.append("")
        lines.append("| Date | Venue | Title | Slides |")
        lines.append("|---|---|---|---|")
        for e in rows:
            date = e.get("date", "")
            venue = e.get("venue_name") or e.get("venue", "")
            title = e.get("title", "")
            pdf = e.get("pdf", "")
            slides = f"[PDF]({pdf})" if pdf else "_TBD_"
            lines.append(f"| {date} | {venue} | {title} | {slides} |")
        lines.append("")
    return "\n".join(lines).rstrip("\n")


def render_readme(current: str, tables: str) -> str:
    if BEGIN not in current or END not in current:
        sys.exit(
            f"error: README.md is missing the {BEGIN!r} / {END!r} markers; "
            "cannot locate the generated section."
        )
    head, rest = current.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    return f"{head}{BEGIN}\n{tables}\n{END}{tail}"


def main(argv: list[str]) -> int:
    check = "--check" in argv[1:]

    entries = load_entries()
    tables = build_tables(entries)
    current = README_FILE.read_text()
    expected = render_readme(current, tables)

    if check:
        if current != expected:
            print(
                "README.md is out of date with metadata/events.yml.\n"
                "Run `python3 scripts/generate_readme.py` and commit the result.",
                file=sys.stderr,
            )
            return 1
        print("OK: README.md is in sync with metadata/events.yml.")
        return 0

    if current != expected:
        README_FILE.write_text(expected)
        print("Updated README.md from metadata/events.yml.")
    else:
        print("README.md already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
