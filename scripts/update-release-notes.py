#!/usr/bin/env python3
"""Refresh the three release-note pages from published release changelogs."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/docs/release-notes"
PROJECTS = (
    ("msl", "msl.md", "MSL release"),
    ("msl-kernel", "kernel.md", "Linux kernel release"),
    ("msl-vscode-extension", "vscode.md", "MSL VS Code extension release"),
)
SECTION = re.compile(r"(?m)^## \[([^\]]+)\][^\n]*\n")
PAGE_RELEASE = re.compile(r"(?m)^## (\S+)\s*$")


@dataclass(frozen=True)
class Release:
    repo: str
    tag: str
    published_at: str
    url: str
    prerelease: bool


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


def latest_release(repo: str) -> Release:
    url = f"https://api.github.com/repos/onexay/{repo}/releases?per_page=100"
    data = json.loads(request_text(url))
    if not isinstance(data, list):
        raise RuntimeError(f"GitHub did not return a release list for onexay/{repo}")
    releases = [item for item in data if not item.get("draft") and item.get("published_at")]
    if not releases:
        raise RuntimeError(f"Repository onexay/{repo} has no published releases")
    item = max(releases, key=lambda release: release["published_at"])
    return Release(
        repo,
        item["tag_name"],
        item["published_at"],
        item["html_url"],
        item.get("prerelease", False),
    )


def changelog_section(changelog: str, repo: str, tag: str) -> str:
    matches = list(SECTION.finditer(changelog))
    sections = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(changelog)
        sections.append((match.group(1).strip(), changelog[match.end():end].strip()))

    tag_names = {tag, tag.removeprefix("v")}
    if repo == "msl":
        selected = next((body for name, body in sections if name.lower() == "unreleased"), "")
        if not selected:
            selected = next((body for name, body in sections if name in tag_names), "")
    else:
        selected = next((body for name, body in sections if name in tag_names), "")
        if not selected:
            selected = next((body for name, body in sections if name.lower() == "unreleased"), "")

    if not selected:
        raise RuntimeError(
            f"CHANGELOG.md in onexay/{repo}@{tag} has no non-empty Unreleased "
            "section or section matching the release tag"
        )
    return selected


def release_block(release: Release, description: str) -> str:
    date = datetime.fromisoformat(release.published_at.replace("Z", "+00:00")).strftime("%-d %B %Y")
    status = "**Pre-release** · " if release.prerelease else ""
    changelog_url = (
        f"https://raw.githubusercontent.com/onexay/{release.repo}/"
        f"{quote(release.tag, safe='')}/CHANGELOG.md"
    )
    notes = changelog_section(request_text(changelog_url), release.repo, release.tag)
    return (
        f"## {release.tag}\n\n"
        f"{status}{description} · {date} · [GitHub release]({release.url})\n\n"
        f"{notes}\n"
    )


def main() -> int:
    releases = [latest_release(repo) for repo, _, _ in PROJECTS]
    updates: list[tuple[Path, str, str]] = []

    # Validate and render every changed page before writing any of them.
    for (repo, filename, description), release in zip(PROJECTS, releases, strict=True):
        path = NOTES / filename
        original = path.read_text(encoding="utf-8")
        first = PAGE_RELEASE.search(original)
        if first and first.group(1) == release.tag:
            print(f"{path.relative_to(ROOT)} already documents {release.tag}")
            continue

        block = release_block(release, description)
        if first:
            insertion = first.start()
            prefix, previous_releases = original[:insertion], original[insertion:]
            updated = prefix.rstrip() + "\n\n" + block + "\n" + previous_releases.lstrip()
        else:
            updated = original.rstrip() + "\n\n" + block
        updates.append((path, original, updated.rstrip() + "\n"))

    for path, original, updated in updates:
        if original != updated:
            path.write_text(updated, encoding="utf-8")
            print(f"Updated {path.relative_to(ROOT)}")

    if not updates:
        print("Release notes are current.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, json.JSONDecodeError, OSError, ValueError) as error:
        print(f"release notes: {error}", file=sys.stderr)
        raise SystemExit(1)
