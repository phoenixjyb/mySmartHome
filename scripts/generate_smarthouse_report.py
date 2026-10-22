#!/usr/bin/env python3
"""Build the self-contained SmartHouse procurement and network report."""
from __future__ import annotations

import csv
import html
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "inventory/procurement_2026-10-22.csv"
TEMPLATE_PATH = ROOT / "scripts/templates/smarthouse_report.html"
OUTPUT_PATH = ROOT / "exports/智能家居采购与网络架构_2026-10-22.html"
FIRST_ORDER_IDS = ("ZB-COORD", "ZB-TH", "ZB-WATER", "ZB-DOOR", "ZB-PIR", "ZB-PRES", "ZB-BUTTON", "ZB-PLUG")


def esc(value: object) -> str:
    return html.escape(str(value or "").strip(), quote=True)


def safe_url(value: str) -> str:
    value = (value or "").strip()
    parts = urlsplit(value)
    if parts.scheme in {"http", "https"} and parts.netloc:
        return value
    return ""


def bucket(row: dict[str, str]) -> str:
    code = row["编号"]
    core = {"NET-ROUTER", "NET-SWITCH", "NET-AP", "BUS-GW", "RACK", "PDU", "UPS", "PATCH", "CORDS", "SHELF", "HOST", "BACKUP"}
    zigbee = {"ZB-COORD", "ZB-TH", "ZB-WATER", "ZB-DOOR", "ZB-PIR", "ZB-PRES", "ZB-BUTTON", "ZB-PLUG", "ZB-ROUTER"}
    if code in core:
        return "核心网络"
    if code in zigbee:
        return "Zigbee"
    if code in {"CURTAIN", "WALL-SWITCH", "FAN-ACT"}:
        return "窗帘照明"
    return "安全配件"


def state(row: dict[str, str]) -> str:
    s = row["采购状态"]
    if "可先购" in s or "可先买" in s:
        return "可先买"
    if row["已购数量"] not in ("", "0"):
        return "已有"
    if "后期" in s or "入住后" in s or "覆盖实测后" in s or ("覆盖" in s and "补" in s):
        return "后期"
    return "待确认"


def render_card(row: dict[str, str]) -> str:
    cat, st = bucket(row), state(row)
    url = safe_url(row["京东入口"])
    link = f'<a class="buy-link" href="{esc(url)}" target="_blank" rel="noreferrer noopener">打开京东候选 ↗</a>' if url else ""
    label = row["候选型号"]
    qty = row["首批计划数量"]
    final_qty = row["最终目标数量"]
    existing = row["已购数量"] or "0"
    return f'''<article class="item" data-category="{esc(cat)}" data-state="{esc(st)}" data-search="{esc(' '.join(row.values()).lower())}">
      <div class="item-top"><span class="id">{esc(row['编号'])}</span><span class="pill {esc(st)}">{esc(st)}</span></div>
      <h3>{esc(row['类别'])}</h3><p class="model">{esc(label)}</p>
      <div class="quantities"><div><b>{esc(qty)}</b><small>首批建议</small></div><div><b>{esc(final_qty)}</b><small>最终目标</small></div><div><b>{esc(existing)}</b><small>已购记录</small></div></div>
      <p class="room">⌖ {esc(row['安装区域'])}</p>{link}
      <details><summary>付款前条件与验收</summary><div class="detail-copy"><b>付款前</b><p>{esc(row['付款前条件'])}</p><b>到货后验收</b><p>{esc(row['验收要点'])}</p></div></details>
    </article>'''


def main() -> None:
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
    if len(rows) != 29:
        raise SystemExit(f"Expected 29 procurement rows, found {len(rows)}")
    cards = "\n".join(render_card(row) for row in rows)
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    document = template.replace("{{PROCUREMENT_CARDS}}", cards)
    document = document.replace("{{ITEM_COUNT}}", str(len(rows)))
    by_id = {row["编号"]: row for row in rows}
    first_order = []
    for code in FIRST_ORDER_IDS:
        row = by_id[code]
        url = safe_url(row["京东入口"])
        if not url.startswith("https://item.jd.com/"):
            raise SystemExit(f"First-order item requires a direct JD link: {code}")
        first_order.append(f'<tr><td>{esc(row["类别"])}</td><td>{esc(row["候选型号"])}</td>'
                           f'<td>{esc(row["首批计划数量"])}</td><td><a href="{esc(url)}" '
                           'target="_blank" rel="noreferrer noopener">打开商品 ↗</a></td></tr>')
    document = document.replace("{{FIRST_ORDER_ROWS}}", "\n".join(first_order))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(document, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
