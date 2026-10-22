#!/usr/bin/env python3
"""Generate the offline laundry research view from the archived Markdown report.

Run from any directory: python3 scripts/generate_laundry_report.py
No third-party packages or network requests are needed.
"""

from __future__ import annotations

import base64
import hashlib
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM = "北京洗烘套装选型_600与610mm及博西C档_2026-10-22"
SOURCE = ROOT / "docs/current" / f"{STEM}.md"
EVIDENCE = ROOT / "references/洗烘套装选型_2026-10-22"
OUTPUT = ROOT / "exports/北京洗烘套装选型_2026-10-22.html"
TEMPLATE = ROOT / "scripts/templates/laundry_report.html"

# This overview is a dated editorial summary; the complete Markdown source below
# remains available in the HTML. Updating the research requires reviewing both.
CANDIDATES = [
    dict(name="松下 M2", tag="优先核实", tier="ab", tone="amber", capacity="10kg洗 · 10kg热泵烘",
         washer="XQG100-M2Q1", dryer="NH-M2QR1", value="630 × 560 × 1722", unit="mm · 厂家专属建议开口：宽 × 深 × 高",
         finding="开口图与现有柜体接近，但机器505／550mm深度明确不含门，尚不能认定安装总深满足600或610mm。",
         stock="当日北京页面：可配送", stock_tone="green",
         note="补贴价约¥10,643，含资格和券条件。专属开口图与通用侧边留空要求有口径差异，需厂家确认。",
         url="https://item.jd.com/100215421700.html", link="京东自营商品页", evidence="panasonic"),
    dict(name="海尔 云溪4.0Pro 75DW", tag="B档重点候选", tier="b", tone="green", capacity="10kg洗 · 10kg热泵烘",
         washer="XQG100-BLEG75DWU1", dryer="GA100-STQ75DWU1", value="607", unit="mm · 两机背后均留30mm时的深度计算值",
         finding="烘干机含门577＋背部30＝607。洗衣机后方要求≥30mm；两台均按30mm核对，距B档上限仅余3mm。",
         stock="有效SKU与北京配送待核", stock_tone="amber",
         note="净宽至少625mm；按约1750mm开口，叠架和调平变化合计空间约30mm，成套总高仍待确认。",
         url="https://www.jd.com/jiage/73763cfab7fc13ceb2e.html", link="京东目录线索 · 非现货承诺", evidence="haier-washer"),
    dict(name="TCL 双子舱 T10", tag="B档边界候选", tier="b", tone="green", capacity="10kg洗 · 10kg热泵烘 · 双筒塔",
         washer="GH200T10-W", dryer="集成双筒洗烘塔", value="610", unit="mm · 含门580＋厂家背部预留30",
         finding="深度计算正好到B档边界。建议开口宽625、高1700mm；现场接头和管线须收在厂家背部预留内。",
         stock="当日北京页面：暂时售完", stock_tone="red",
         note="这是洗、烘各自独立的双筒热泵塔。其他颜色、P10或新型号的尺寸和库存不可套用。",
         url="https://item.jd.com/100069014789.html", link="京东自营商品页", evidence="tcl"),
    dict(name="东芝 玉兔2.0 T19", tag="B档边界候选", tier="b", tone="amber", capacity="10kg洗 · 10kg热泵烘",
         washer="DG-10T19BI", dryer="DH-10T19B", value="610", unit="mm · 仅洗衣机最大580＋后留30",
         finding="烘干机厂家对比图标新款安装深600mm；整套仍缺叠架后高度和烘干机完整含门／管线定义。",
         stock="北京有效自营SKU未确认", stock_tone="amber",
         note="厂家商城已下架。图中“突出30mm”属于左侧旧款，不能加在右侧新款上。",
         url="https://www.midea.cn/395/1000000000400701586424.html", link="厂家精确型号资料 · 已下架", evidence="toshiba"),
    dict(name="西门子 小幸熨超薄", tag="C档 · 白色备选", tier="c", tone="blue", capacity="10kg洗 · 10kg热泵烘",
         washer="WW52J7Y00W", dryer="WT52J7Y01W", value="610 + r", unit="mm · 洗衣机最大外廓＋额外后留空",
         finding="洗衣机宽598、机身名义深565、最大外廓610。适合作为放宽尺寸后的白色候选，并非已满足B档。",
         stock="京东自营套装 · 北京现货待核", stock_tone="amber",
         note="后留空r尚未核实；烘干机完整外廓、原装叠架总高仍待确认。WW52型号不可与WG52混淆。",
         url="https://item.jd.com/100248516603.html", link="京东自营套装", evidence="siemens"),
    dict(name="博世 摩德纳Slim", tag="C档 · 星云灰备选", tier="c", tone="blue", capacity="10kg洗 · 10kg热泵烘",
         washer="WWJ752Y10W", dryer="WTJ752Y11W", value="610 + r", unit="mm · 洗衣机最大外廓＋额外后留空",
         finding="已核洗衣机尺寸与西门子这款相同，没有证据说明两套中哪套明显更薄；可按灰色外观偏好保留。",
         stock="京东套装页面 · 北京现货待核", stock_tone="amber",
         note="565mm不是成套安装总深。烘干机和叠架仍须核实，WWJ型号不可与WGJ混淆。",
         url="https://item.jd.com/100391506596.html", link="京东套装商品页", evidence="bosch"),
]

GALLERY = [
    ("cabinet", "定制柜尺寸-用户提供.jpg", "原始柜体尺寸", "用户提供的图纸", "净宽约630mm、设备区约1750mm为图纸初读；完成面和板厚尚待核实。"),
    ("panasonic", "松下M2-叠放安装尺寸.png", "松下M2 · 专属叠放开口", "京东商品详情原图", "630 × 560 × 1722mm是建议开口；560未明确等于含门、含管线的安装总深。"),
    ("panasonic-body", "松下M2-不含门尺寸.png", "松下M2 · 不含门尺寸", "同一精确套装商品图", "洗衣机505、烘干机550，明确不含机门，不能直接拿来判断A／B档。"),
    ("panasonic-generic", "松下-通用安装须知.png", "松下 · 通用留空要求", "同一京东详情页", "通用侧边各20mm与专属630mm宽开口存在口径差异，需厂家按精确型号确认。"),
    ("tcl", "TCL-T10-含门和后留空.jpg", "TCL T10 · 含门及后留空", "厂家安装图", "580mm含门＋30mm后方预留＝610mm；是B档纸面计算值，不等于现场已验收。"),
    ("toshiba", "东芝T19烘干机-新旧款安装对比.jpg", "东芝T19 · 新旧款对比", "厂家烘干机详情图", "左边旧款的“突出30mm”与右边新款“安装深度600mm”分开读取。"),
    ("haier-washer", "海尔75DW-洗衣机安装留空.png", "海尔75DW · 洗衣机留空", "精确型号原厂H5说明书", "后方≥30mm，左右各≥15mm，上方≥20mm。尺寸值需结合精确型号表。"),
    ("haier-dryer", "海尔75DW-烘干机安装留空.png", "海尔75DW · 烘干机留空", "精确型号原厂H5说明书", "后方≥10mm，左右各≥15mm，上方≥20mm。报告保守按两机背后都留30mm计算。"),
    ("haier-depth", "海尔75DW-含门尺寸示意.png", "海尔75DW · 深度口径", "原厂H5示意图", "D1为关闭机门的外廓参考；本图不带数值，577mm须结合归档的精确型号数据表。"),
    ("siemens", "西门子WW52J7Y00W-尺寸图.png", "西门子 · 565与610", "归档原厂PDF尺寸页", "WW52J7Y00W的565为名义机身深度，610为最大外廓；额外后留空尚未确认。"),
    ("bosch", "博世WWJ752Y10W-尺寸图.png", "博世 · 565与610", "归档原厂PDF尺寸页", "WWJ752Y10W与所选西门子洗衣机外廓相同；不要把洗衣机外廓当整套安装总深。"),
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def image_uri(filename: str) -> str:
    path = EVIDENCE / filename
    mime = "image/png" if path.suffix == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def inline(text: str) -> str:
    # All input is escaped before restoring the limited Markdown subset used in
    # the archived report. The report contains no raw HTML or executable content.
    text = esc(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                  lambda m: f'<a href="{m[2]}"' + (' target="_blank" rel="noopener noreferrer"' if m[2].startswith("https://") else '') + f'>{m[1]}</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", text)


def cells(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]


def render_markdown(source: str) -> str:
    lines, result, index = source.splitlines(), [], 0
    by_filename = {name: key for key, name, *_ in GALLERY}
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith("```"):
            index += 1
            code = []
            while index < len(lines) and not lines[index].startswith("```"):
                code.append(lines[index]); index += 1
            result.append("<pre><code>" + esc("\n".join(code)) + "</code></pre>"); index += 1
        elif line.startswith("|"):
            header = cells(line); index += 2
            rows = []
            while index < len(lines) and lines[index].startswith("|"):
                rows.append("<tr>" + "".join("<td>" + inline(c) + "</td>" for c in cells(lines[index])) + "</tr>")
                index += 1
            result.append('<div class="table-wrap" tabindex="0"><table><thead><tr>' + "".join("<th>" + inline(c) + "</th>" for c in header) + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>")
        elif match := re.match(r"^(#{1,3}) (.+)$", line):
            level = min(len(match[1]) + 1, 4)
            result.append(f"<h{level}>{inline(match[2])}</h{level}>"); index += 1
        elif match := re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line):
            key = by_filename[Path(match[2]).name]
            result.append(f'<p><a href="#evidence-{key}">查看已归档安装图：{esc(match[1])} ↗</a></p>'); index += 1
        elif line.startswith("- "):
            items = []
            while index < len(lines) and lines[index].startswith("- "):
                items.append("<li>" + inline(lines[index][2:]) + "</li>"); index += 1
            result.append("<ul>" + "".join(items) + "</ul>")
        else:
            paragraph = [line]; index += 1
            while index < len(lines) and lines[index].strip() and not re.match(r"^(?:#{1,3} |\||- |```|!\[)", lines[index]):
                paragraph.append(lines[index]); index += 1
            result.append("<p>" + inline(" ".join(paragraph)) + "</p>")
    return "\n".join(result)


def main() -> None:
    source = SOURCE.read_text()
    # Markdown links are relative to docs/current; HTML lives one level higher.
    web_source = source.replace("](../../", "](../")
    brand_section = web_source.split("## 19品牌覆盖与排除记录", 1)[1].split("## 已完成", 1)[0]
    brand_rows = [cells(line) for line in brand_section.splitlines() if line.startswith("|")][2:]
    assert len(brand_rows) == 19, "Review the brand table before regenerating."
    cards = []
    for c in CANDIDATES:
        cards.append(f'''<article class="candidate" data-tier="{c['tier']}">
<div class="card-top"><span class="badge {c['tone']}">{c['tag']}</span><span class="capacity">{c['capacity']}</span></div>
<h3>{c['name']}</h3><div class="models">{c['washer']}<br>＋ {c['dryer']}</div>
<div class="dimension">{c['value']}</div><div class="dimension-unit">{c['unit']}</div>
<p class="finding">{c['finding']}</p><p class="stock {c['stock_tone']}"><span aria-hidden="true">●</span> {c['stock']}</p><p class="card-note">{c['note']}</p>
<div class="card-links"><a href="{c['url']}" target="_blank" rel="noopener noreferrer">{c['link']} ↗</a><a href="#evidence-{c['evidence']}">尺寸证据 ↓</a></div></article>''')
    gallery = []
    for key, filename, title, origin, caption in GALLERY:
        gallery.append(f'''<figure class="evidence" id="evidence-{key}">
<button class="image-button" type="button" data-title="{esc(title)}" aria-label="放大：{esc(title)}"><img src="{image_uri(filename)}" alt="{esc(title)}" loading="lazy" decoding="async"><span class="zoom-label">查看大图 ↗</span></button>
<figcaption><span class="eyebrow">{esc(origin)}</span><h3>{esc(title)}</h3><p>{esc(caption)}</p></figcaption></figure>''')
    table_rows = []
    for row in brand_rows:
        table_rows.append('<tr class="brand-row">' + ''.join('<td>' + inline(c) + '</td>' for c in row) + '</tr>')
    replacements = {
        "@@SOURCE_HASH@@": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "@@SOURCE_LINK@@": f"../docs/current/{STEM}.md",
        "@@CABINET_IMAGE@@": image_uri("定制柜尺寸-用户提供.jpg"),
        "@@CANDIDATES@@": "\n".join(cards),
        "@@GALLERY@@": "\n".join(gallery),
        "@@BRAND_ROWS@@": "\n".join(table_rows),
        "@@FULL_REPORT@@": render_markdown(web_source),
    }
    page = TEMPLATE.read_text()
    for token, value in replacements.items():
        assert token in page, token
        page = page.replace(token, value)
    assert not re.search(r"@@[A-Z_]+@@", page), "Unfilled template token"
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(page)
    print(f"Generated {OUTPUT.relative_to(ROOT)} ({len(page.encode()):,} bytes; {len(GALLERY)} embedded images; 19 brands)")


if __name__ == "__main__":
    main()
