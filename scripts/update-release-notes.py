#!/usr/bin/env python3
"""Add unpublished GitHub releases to the docs release-note pages."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/docs/release-notes"
PROJECTS = (
    ("msl", "msl.md", "MSL release"),
    ("msl-kernel", "kernel.md", "Linux kernel release"),
    ("msl-vscode-extension", "vscode.md", "MSL VS Code extension release"),
)
RELEASE_HEADING = re.compile(r"(?m)^## (.+?)\s*$")
RELEASE_METADATA = re.compile(r"(?mi)^Install:\s|^\|\s*\|\s*\|\s*$")


@dataclass(frozen=True)
class Release:
    tag: str
    published_at: str
    url: str
    body: str
    prerelease: bool

    @property
    def published_datetime(self) -> datetime:
        return datetime.fromisoformat(self.published_at.replace("Z", "+00:00"))


def request_text(url: str) -> str:
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "msl-docs-release-notes",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8")
    except (HTTPError, URLError, TimeoutError) as error:
        raise RuntimeError(f"Could not fetch {url}: {error}") from error


def published_releases(repo: str) -> list[Release]:
    releases: list[Release] = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/onexay/{repo}/releases?per_page=100&page={page}"
        data = json.loads(request_text(url))
        if not isinstance(data, list):
            raise RuntimeError(f"GitHub did not return a release list for onexay/{repo}")
        if not data:
            break
        for item in data:
            if item.get("draft") or not item.get("published_at"):
                continue
            releases.append(
                Release(
                    item["tag_name"],
                    item["published_at"],
                    item["html_url"],
                    (item.get("body") or "").strip(),
                    item.get("prerelease", False),
                )
            )
        if len(data) < 100:
            break
        page += 1
    return sorted(releases, key=lambda release: release.published_datetime, reverse=True)


def is_documented(page: str, tag: str) -> bool:
    return bool(re.search(rf"(?m)^## {re.escape(tag)}\s*$", page))


def release_notes(body: str) -> str:
    metadata = RELEASE_METADATA.search(body)
    return body[:metadata.start()].strip() if metadata else body.strip()


def release_block(release: Release, description: str) -> str:
    notes = release_notes(release.body)
    if not notes:
        raise RuntimeError(
            f"Release {release.tag} at {release.url} has no release notes before "
            "its install and asset metadata; publish it with generated notes before syncing"
        )
    date = release.published_datetime.strftime("%d %B %Y").lstrip("0")
    status = "**Pre-release** · " if release.prerelease else ""
    return (
        f"## {release.tag}\n\n"
        f"{status}{description} · {date} · [GitHub release]({release.url})\n\n"
        f"{notes}\n"
    )


def updated_page(original: str, releases: list[Release], description: str) -> tuple[str, int]:
    missing = [release for release in releases if not is_documented(original, release.tag)]
    if not missing:
        return original, 0

    # Validate all new release bodies before writing any page.
    blocks = [release_block(release, description) for release in missing]
    known_tags = {
        release.tag for release in releases
        if is_documented(original, release.tag)
    }
    insertion = next(
        (
            match.start()
            for match in RELEASE_HEADING.finditer(original)
            if match.group(1) in known_tags
        ),
        len(original),
    )
    prefix, previous = original[:insertion], original[insertion:]
    updated = prefix.rstrip() + "\n\n" + "\n".join(block.rstrip() for block in blocks)
    if previous.strip():
        updated += "\n\n" + previous.lstrip()
    return updated.rstrip() + "\n", len(missing)


def main() -> int:
    # Prepare every page first so one empty release body cannot cause a partial update.
    prepared: list[tuple[Path, str, str, int]] = []
    for repo, filename, description in PROJECTS:
        releases = published_releases(repo)
        path = NOTES / filename
        original = path.read_text(encoding="utf-8")
        updated, count = updated_page(original, releases, description)
        if count:
            prepared.append((path, original, updated, count))
        else:
            print(f"{path.relative_to(ROOT)} already includes all published releases")

    for path, original, updated, count in prepared:
        if original != updated:
            path.write_text(updated, encoding="utf-8")
            print(f"Added {count} release(s) to {path.relative_to(ROOT)}")

    if not prepared:
        print("Release notes are current.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, json.JSONDecodeError, OSError, ValueError) as error:
        print(f"release notes: {error}", file=sys.stderr)
        raise SystemExit(1)
