#!/usr/bin/env python3
"""Rebuild the index and the exploration headers from the metadata files.

    python tools/build_index.py            rewrite what is out of date
    python tools/build_index.py --check    report only, exit 1 if anything differs

Single source of truth: explorations/NNN-.../metadata.yml. This script rewrites the table in
the main README between the index markers, and the header block of each exploration page
between the meta markers, then checks that the expected files and local links exist.
Standard library only: the metadata is flat "key: value", so it needs no YAML parser.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPLORATIONS = ROOT / "explorations"

STATUS = {
    "unverified": ("🟠", "Unverified"),
    "partially-verified": ("🟡", "Partially verified"),
    "verified": ("🟢", "Verified"),
    "refuted": ("🔴", "Refuted"),
    "superseded": ("⚪", "Superseded"),
}

REQUIRED_KEYS = ("id", "title", "date", "area", "status", "ai_system", "published_by")
REQUIRED_FILES = ("README.md", "exploration.pdf", "source.tex", "ai-output.md")

problems = []


def fail(where, message):
    problems.append(f"{where}: {message}")


def read_metadata(path):
    data = {}
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip() if not raw.strip().startswith("#") else ""
        if not line:
            continue
        if ":" not in line:
            fail(path.relative_to(ROOT), f"line {number} is not 'key: value'")
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    for key in REQUIRED_KEYS:
        if not data.get(key):
            fail(path.relative_to(ROOT), f"missing '{key}'")
    if data.get("status") not in STATUS:
        fail(path.relative_to(ROOT), f"unknown status {data.get('status')!r}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", data.get("date", "")):
        fail(path.relative_to(ROOT), "date must be YYYY-MM-DD")
    return data


def badge(status):
    symbol, label = STATUS.get(status, ("", status))
    return f"{symbol} {label}"


def header_block(meta):
    interface = f" — via {meta['interface']}" if meta.get("interface") else ""
    lines = [
        f"# {meta['title']}",
        "",
        f"**Status:** {badge(meta['status'])} \\",
        f"**Area:** {meta['area']} \\",
        f"**Date:** {meta['date']} \\",
        f"**AI system:** {meta['ai_system']}{interface} \\",
        f"**Published by:** {meta['published_by']}",
    ]
    for key, text in (("supersedes", "Supersedes"), ("superseded_by", "Superseded by")):
        if meta.get(key):
            lines.append(f" \\\n**{text}:** exploration {meta[key]}")
    return "\n".join(lines)


def splice(text, name, replacement, where):
    start, end = f"<!-- {name}:start -->", f"<!-- {name}:end -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pattern.search(text):
        fail(where, f"missing {start} / {end} markers")
        return text
    return pattern.sub(f"{start}\n{replacement}\n{end}", text, count=1)


def write(path, new_text, check_only):
    if path.read_text(encoding="utf-8") == new_text:
        return False
    if check_only:
        fail(path.relative_to(ROOT), "out of date, run tools/build_index.py")
    else:
        path.write_text(new_text, encoding="utf-8", newline="\n")
        print(f"updated {path.relative_to(ROOT)}")
    return True


def check_links(path):
    """Local links only: anything that resolves outside the repository is a GitHub route."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = target.split("#", 1)[0]
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            continue
        if not resolved.exists():
            fail(path.relative_to(ROOT), f"broken link -> {target}")


def main():
    check_only = "--check" in sys.argv
    directories = sorted(
        d for d in EXPLORATIONS.iterdir() if d.is_dir() and not d.name.startswith("_")
    )

    rows, seen = [], {}
    for directory in directories:
        metadata_file = directory / "metadata.yml"
        if not metadata_file.exists():
            fail(directory.relative_to(ROOT), "no metadata.yml")
            continue
        meta = read_metadata(metadata_file)
        if not meta.get("id"):
            continue
        if meta["id"] in seen:
            fail(directory.relative_to(ROOT), f"id {meta['id']} already used by {seen[meta['id']]}")
        seen[meta["id"]] = directory.name

        for name in REQUIRED_FILES:
            if not (directory / name).exists():
                fail(directory.relative_to(ROOT), f"missing {name}")

        page = directory / "README.md"
        if page.exists():
            write(page, splice(page.read_text(encoding="utf-8"), "meta", header_block(meta),
                               page.relative_to(ROOT)), check_only)

        link = f"explorations/{directory.name}/"
        rows.append(
            f"| [{meta['id']}]({link}) | {meta['title']} | {meta['area']} "
            f"| {badge(meta['status'])} | {meta['date']} |"
        )

    table = "\n".join(
        ["| # | Exploration | Area | Status | Date |", "| --- | --- | --- | --- | --- |"] + rows
    ) if rows else "_No explorations yet._"

    readme = ROOT / "README.md"
    write(readme, splice(readme.read_text(encoding="utf-8"), "index", table, "README.md"),
          check_only)

    for path in sorted(ROOT.rglob("*.md")):
        # the template links to files that only exist once it is copied
        if not any(part == ".git" or part.startswith("_") for part in path.parts):
            check_links(path)

    if problems:
        print("\n".join(f"problem: {p}" for p in problems))
        return 1
    print(f"{len(rows)} exploration(s) indexed, links and files check out.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
