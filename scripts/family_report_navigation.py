"""Shared static return-home control for the six published family reports."""
from __future__ import annotations

import re

STYLE_START = "<!-- family-home-navigation-style:start -->"
STYLE_END = "<!-- family-home-navigation-style:end -->"
NAV_START = "<!-- family-home-navigation:start -->"
NAV_END = "<!-- family-home-navigation:end -->"

STYLE = '''<style id="family-home-navigation-style">
body{padding-bottom:calc(76px + env(safe-area-inset-bottom,0px))}
#family-home-navigation{position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:900;margin:0;padding:0}
#family-home-navigation a{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:44px;padding:10px 17px;border:1px solid #9cab99;border-radius:999px;background:#fffdf8;color:#315b49;box-shadow:0 4px 18px #26342b24;font:600 14px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;letter-spacing:0;text-decoration:none;white-space:nowrap}
#family-home-navigation a:hover{background:#e9efe3;border-color:#315b49}
#family-home-navigation a:focus-visible{outline:3px solid #a16b45;outline-offset:4px}
#family-home-navigation svg{display:block;width:18px;height:18px;flex-shrink:0;fill:none;stroke:currentColor;stroke-width:1.6}
@media(max-width:600px){#family-home-navigation a{padding:10px 14px;font-size:13px}}
@media print{#family-home-navigation{display:none}body{padding-bottom:0}}
</style>'''


def strip_home_navigation(document: str) -> str:
    """Remove only this control's marked fragments, preserving report content."""
    for start, end in ((STYLE_START, STYLE_END), (NAV_START, NAV_END)):
        if document.count(start) != document.count(end) or document.count(start) > 1:
            raise ValueError("Ambiguous family-home navigation markers")
        document = re.sub(re.escape(start) + r".*?" + re.escape(end), "", document, flags=re.S)
    return document


def with_home_navigation(document: str, home_href: str) -> str:
    """Add an idempotent, keyboard-accessible control using a fixed relative URL."""
    if home_href not in {"home/index.html", "../home/index.html"}:
        raise ValueError("Expected an approved relative family-home route")
    document = strip_home_navigation(document)
    if len(re.findall(r"</head\s*>", document, flags=re.I)) != 1:
        raise ValueError("Expected one closing head element")
    if len(re.findall(r"</body\s*>", document, flags=re.I)) != 1:
        raise ValueError("Expected one closing body element")
    if re.search(r'id=[\"\']family-home-navigation(?:-style)?[\"\']', document):
        raise ValueError("Unmarked family-home navigation already exists")
    nav = (f'<nav id="family-home-navigation" aria-label="报告间导航">'
           f'<a href="{home_href}"><svg viewBox="0 0 24 24" aria-hidden="true">'
           '<path d="M3 11 12 4l9 7M6 9v11h12V9M10 20v-7h4v7"/>'
           '</svg><span>返回总首页</span></a></nav>')
    document = re.sub(r"</head\s*>", lambda m: STYLE_START + STYLE + STYLE_END + m[0], document, count=1, flags=re.I)
    return re.sub(r"</body\s*>", lambda m: NAV_START + nav + NAV_END + m[0], document, count=1, flags=re.I)
