#!/usr/bin/env python3
"""Package the family report navigation page; no connection or live publication."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "exports/新家报告导航首页_2026-10-22.html"
REPORT_LINKS = (
    "../kitchen-20261022/index.html",
    "../laundry-20261022/index.html",
    "../smart-home-20261022/index.html",
    "../v3/index.html",
    "../v2/index.html",
    "../index.html",
)


class Page(HTMLParser):
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
        if tag in {"script", "iframe", "object", "embed", "base"}:
            raise ValueError("Navigation page must remain static and self-contained")
        if tag in {"img", "link"} and (attrs.get("src") or attrs.get("href")):
            raise ValueError("External or file assets require review")


def package(destination: Path) -> dict:
    if destination.exists():
        raise ValueError("Use a new package directory")
    body = SOURCE.read_bytes()
    source = body.decode("utf-8")
    if any(value in source for value in ("/Users/", "file://", "C:\\", "/family-design/")):
        raise ValueError("Private deployment data in page")
    if re.search(r"url\s*\(|@import", source, re.I):
        raise ValueError("CSS asset dependency requires review")
    page = Page()
    page.feed(source)
    report_links = [link for link in page.links if not link.startswith("#")]
    if tuple(report_links) != REPORT_LINKS:
        raise ValueError("Expected exactly the six approved report routes, in order")
    for link in page.links:
        if link.startswith("#") and link[1:] not in page.ids:
            raise ValueError("Broken page anchor")
    destination.mkdir(parents=True)
    (destination / "index.html").write_bytes(body)
    entry = {"path": "index.html", "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}
    (destination / "manifest.json").write_text(json.dumps({"format": 1, "files": [entry]}, indent=2) + "\n")
    return {"payloads": 1, **entry, "report_links": len(report_links)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    print(json.dumps(package(parser.parse_args().destination.resolve()), indent=2))
