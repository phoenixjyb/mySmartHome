#!/usr/bin/env python3
"""Prepare the laundry HTML for the existing allowlisted Windows static site.

This only creates a local public package. It does not connect to a host, select
a live share link, publish files or change scheduled tasks.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from family_report_navigation import with_home_navigation

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "exports/北京洗烘套装选型_2026-10-22.html"


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "img" and attrs.get("src"):
            self.images.append(attrs["src"])
        if tag == "a":
            self.links.append(attrs.get("href", ""))


def package(destination: Path) -> dict:
    if destination.exists():
        raise ValueError("Choose a new package directory; existing files are preserved.")
    page = SOURCE.read_text()
    if "/Users/" in page or "file://" in page:
        raise ValueError("Host-local path in source HTML")
    destination.mkdir(parents=True)
    images = destination / "images"
    images.mkdir()
    files = {}

    def extract_image(match):
        kind, encoded = match.groups()
        body = base64.b64decode(encoded, validate=True)
        if kind == "png" and not body.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("Invalid PNG payload")
        if kind == "jpeg" and not body.startswith(b"\xff\xd8\xff"):
            raise ValueError("Invalid JPEG payload")
        digest = hashlib.sha256(body).hexdigest()
        name = "images/" + digest[:24] + (".png" if kind == "png" else ".jpg")
        if name in files and files[name] != body:
            raise ValueError("Image-name collision")
        files[name] = body
        return name

    page = re.sub(r"data:image/(png|jpeg);base64,([A-Za-z0-9+/=]+)", extract_image, page)
    if len(files) != 11 or "data:image/" in page:
        raise ValueError("Review the image inventory before packaging")

    def public_link(match):
        href = match[1]
        if href.startswith(("https://", "#")):
            return match[0]
        if href.startswith("../docs/") or href.startswith("../exports/"):
            return 'href="#full-report"'
        if href.startswith("../references/"):
            return 'href="#evidence"'
        raise ValueError("Unexpected public link: " + href)

    page = re.sub(r'href="([^"]*)"', public_link, page)
    page = page.replace("Markdown原始报告 ↗", "完整研究正文 ↓")
    page = page.replace(">Markdown原始报告</a>", ">完整研究正文</a>")
    page = page.replace(">原始证据目录</a>", ">安装图与原始证据</a>")
    page = page.replace(">图文交互版HTML</a>", ">当前图文报告</a>")
    page = page.replace(
        "PDF和原始链接保留在完整研究及证据目录中。",
        "原厂说明书与来源链接保留在下方完整研究正文中。",
    )
    page = page.replace(
        "<script>",
        "<script>\n"
        "document.querySelectorAll('a[href=\"#full-report\"]').forEach(link=>"
        "link.addEventListener('click',()=>{document.getElementById('full-report').open=true}));\n",
        1,
    )
    parsed = PageLinks()
    parsed.feed(page)
    if len(parsed.images) != 12 or set(parsed.images) != set(files):
        raise ValueError("Public image references do not match the allowlist")
    for link in parsed.links:
        if link.startswith("#") and link[1:] and link[1:] not in parsed.ids:
            raise ValueError("Broken public anchor: " + link)
        if not link.startswith(("https://", "#")):
            raise ValueError("Non-public repository link remains")
    files["index.html"] = with_home_navigation(page, "../home/index.html").encode("utf-8")
    entries = []
    for name, body in sorted(files.items()):
        (destination / name).write_bytes(body)
        entries.append(dict(path=name, bytes=len(body), sha256=hashlib.sha256(body).hexdigest()))
    manifest = dict(format=1, files=entries)
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return dict(payloads=len(entries), unique_images=len(entries)-1,
                bytes=sum(e["bytes"] for e in entries),
                source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="New local package directory")
    args = parser.parse_args()
    print(json.dumps(package(args.destination.resolve()), indent=2))


if __name__ == "__main__":
    main()
