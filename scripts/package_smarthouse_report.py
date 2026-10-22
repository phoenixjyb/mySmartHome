#!/usr/bin/env python3
"""Package the sanitized SmartHouse page for the existing Windows static site.

This local command neither connects to Windows nor changes a running service.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from family_report_navigation import with_home_navigation

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "exports/智能家居采购与网络架构_2026-10-22.html"


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag in {"script", "img", "iframe", "link", "object", "embed"}:
            if attrs.get("src") or attrs.get("href") or attrs.get("data"):
                raise ValueError("External or file-based asset requires review")


def package(destination: Path) -> dict:
    if destination.exists():
        raise ValueError("Destination exists; use a new package directory")
    body = SOURCE.read_bytes()
    page = body.decode("utf-8")
    if any(x in page for x in ("/Users/", "file://", "C:\\", "/family-design/")):
        raise ValueError("Private path or deployment data in page")
    if re.search(r"(?:https?:)?//[^\s)]+", " ".join(re.findall(r"url\([^)]*\)", page))):
        raise ValueError("Remote CSS resource requires review")
    parsed = References()
    parsed.feed(page)
    for link in parsed.links:
        if link.startswith("#"):
            if link[1:] and link[1:] not in parsed.ids:
                raise ValueError("Broken anchor: " + link)
        elif not link.startswith("https://"):
            raise ValueError("Only HTTPS source links and page anchors are allowed")
    body = with_home_navigation(page, "../home/index.html").encode("utf-8")
    destination.mkdir(parents=True)
    (destination / "index.html").write_bytes(body)
    manifest = {"format": 1, "files": [{"path": "index.html", "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest()}]}
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return {"payloads": 1, "bytes": len(body), "sha256": manifest["files"][0]["sha256"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    print(json.dumps(package(parser.parse_args().destination.resolve()), indent=2))
