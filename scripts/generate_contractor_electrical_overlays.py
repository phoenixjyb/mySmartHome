#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "references/designer-input/强弱电点位图-original.png"
OUT_DETAIL = ROOT / "diagrams/12_强弱电点位图_业主必要标注.png"
OUT_SIMPLE = ROOT / "diagrams/13_强弱电点位图_施工队简版.png"

FONT_CANDIDATES = [
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]

COLORS = {
    "power": "#f28c22",
    "network": "#1f6fd6",
    "rs485": "#8050d8",
    "water": "#d9364a",
    "curtain": "#15945b",
    "skip": "#707070",
    "ink": "#202020",
    "muted": "#5f6368",
    "panel_bg": "#f8f9fb",
}


def font(size: int) -> ImageFont.FreeTypeFont:
    for candidate in FONT_CANDIDATES:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


F_TITLE = font(44)
F_SUB = font(24)
F_BODY = font(27)
F_SMALL = font(22)
F_MARKER = font(24)
F_MARKER_SMALL = font(20)


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def wrap_by_width(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        trial = current + char
        if text_size(draw, trial, fnt)[0] <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = char
    if current:
        lines.append(current)
    return lines


def draw_box(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    outline: str,
    fill: str = "white",
    width: int = 3,
    radius: int = 10,
) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_title(draw: ImageDraw.ImageDraw, simple: bool) -> None:
    title = "强弱电点位图 - 施工队简版" if simple else "强弱电点位图 - 业主必要标注版"
    sub = "平面图只看编号；说明见右侧。普通点位按设计师原图执行" if simple else "给设计师/装修队：只确认编号点位，未标注的普通插座/开关按设计师原图和电工规范执行"
    draw_box(draw, (38, 24, 1040 if simple else 1120, 108), outline="#111111", fill="white", width=2, radius=14)
    draw.text((62, 36), title, font=F_TITLE, fill=COLORS["ink"])
    draw.text((64, 76), sub, font=F_SUB, fill=COLORS["muted"])


def marker(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    label: str,
    color: str,
    r: int = 24,
    small: bool = False,
) -> None:
    draw.ellipse((x - r, y - r, x + r, y + r), fill=color, outline="white", width=4)
    fnt = F_MARKER_SMALL if small else F_MARKER
    tw, th = text_size(draw, label, fnt)
    draw.text((x - tw / 2, y - th / 2 - 1), label, font=fnt, fill="white")


def note_box(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    text: str,
    color: str,
    max_width: int = 360,
    target: tuple[int, int] | None = None,
) -> tuple[int, int, int, int]:
    lines = []
    for part in text.split("\n"):
        lines.extend(wrap_by_width(draw, part, F_SMALL, max_width))
    h = 18 + len(lines) * 27
    w = min(max_width + 24, max(text_size(draw, line, F_SMALL)[0] for line in lines) + 28)
    box = (x, y, x + w, y + h)
    draw_box(draw, box, outline=color, fill="white", width=2, radius=8)
    ty = y + 9
    for line in lines:
        draw.text((x + 12, ty), line, font=F_SMALL, fill=COLORS["ink"])
        ty += 27
    if target:
        tx, ty2 = target
        anchor_x = x if tx < x else x + w
        anchor_y = y + h // 2
        draw.line((anchor_x, anchor_y, tx, ty2), fill=color, width=3)
    return box


def draw_side_panel(draw: ImageDraw.ImageDraw, start_x: int, h: int, simple: bool) -> None:
    panel = (start_x + 26, 40, start_x + 610, h - 42)
    draw_box(draw, panel, outline="#6b6b6b", fill=COLORS["panel_bg"], width=2, radius=18)
    x = start_x + 58
    y = 78
    draw.text((x, y), "业主额外确认点" if simple else "只需确认这些", font=F_TITLE, fill=COLORS["ink"])
    y += 70

    legends = [
        ("强电", COLORS["power"]),
        ("弱电", COLORS["network"]),
        ("RS-485", COLORS["rs485"]),
        ("水路", COLORS["water"]),
        ("窗帘", COLORS["curtain"]),
        ("不做", COLORS["skip"]),
    ]
    col_w = 185
    for idx, (label, color) in enumerate(legends):
        cx = x + (idx % 3) * col_w
        cy = y + (idx // 3) * 38
        draw.ellipse((cx, cy, cx + 20, cy + 20), fill=color)
        draw.text((cx + 34, cy - 5), label, font=F_SMALL, fill=COLORS["ink"])
    y += 92

    items = [
        ("M1", COLORS["power"], "衣帽间机柜：强电插座 + 弱电汇聚"),
        ("M2", COLORS["power"], "P2S：独立插座；不接 UPS；不留墙网口"),
        ("M3", COLORS["network"], "AP1/AP2：各 1 根 PoE 网线回衣帽间"),
        ("M4", COLORS["network"], "PoE Zigbee：中央高位 1 根网线"),
        ("M5", COLORS["network"], "书房桌位：2 网口 + 大容量插座"),
        ("M6", COLORS["network"], "次卧/儿童房：2 网口 + 插座"),
        ("M7", COLORS["network"], "主卧阳台：至少 1 网口 + 插座"),
        ("M8", COLORS["network"], "影音柜：1 网口 + 多位插座"),
        ("M9", COLORS["power"], "投影/幕布：投影电源 + 影音管；幕布只 220V"),
        ("M10", COLORS["rs485"], "RS-485：从衣帽间机柜预留到空调/加湿接入点；图中仅示意两端"),
        ("M11a/b", COLORS["water"], "次卫洗衣 + 厨下/总水阀：水电可检修"),
        ("M12", COLORS["curtain"], "窗帘盒：每组电机侧 220V 常电"),
    ]
    for label, color, text in items:
        marker(draw, x + 18, y + 17, label, color, r=18, small=len(label) > 3)
        for line in wrap_by_width(draw, text, F_BODY, 500):
            draw.text((x + 58, y), line, font=F_BODY, fill=COLORS["ink"])
            y += 32
        y += 11

    skip_h = 182
    skip_box = (x, h - skip_h - 60, start_x + 572, h - 60)
    draw_box(draw, skip_box, outline="#6b6b6b", fill="white", width=2, radius=10)
    draw.text((x + 20, skip_box[1] + 18), "本轮不要求施工", font=F_BODY, fill=COLORS["muted"])
    skip_lines = [
        "× 入户高位摄像头 / 低位门铃",
        "× P2S 墙面网口",
        "× AP-R / 第 3 个 AP",
        "× CO2、门磁、水浸等电池传感器拉线",
    ]
    ty = skip_box[1] + 62
    for line in skip_lines:
        draw.text((x + 20, ty), line, font=F_SMALL, fill=COLORS["ink"])
        ty += 31


def draw_common_markers(draw: ImageDraw.ImageDraw, detailed: bool) -> None:
    # Blue: network / PoE
    marker(draw, 1255, 610, "M3", COLORS["network"])
    marker(draw, 1900, 705, "M3", COLORS["network"])
    marker(draw, 1485, 620, "M4", COLORS["network"])
    marker(draw, 650, 520, "M5", COLORS["network"])
    marker(draw, 1130, 350, "M6", COLORS["network"])
    marker(draw, 2125, 255, "M7", COLORS["network"])
    marker(draw, 1860, 900, "M8", COLORS["network"])

    # Orange: power / fixed equipment
    marker(draw, 1265, 840, "M1", COLORS["power"])
    marker(draw, 1120, 910, "M2", COLORS["power"])
    marker(draw, 2038, 860, "M9", COLORS["power"])

    # Purple: RS-485 endpoints only. Do not draw exact cable route.
    marker(draw, 1220, 802, "M10", COLORS["rs485"])
    marker(draw, 1535, 425, "M10", COLORS["rs485"])

    # Red: split wet-area checks.
    marker(draw, 1455, 505, "M11a", COLORS["water"], r=30, small=True)
    marker(draw, 655, 832, "M11b", COLORS["water"], r=30, small=True)

    # Green: curtain motor power. Multiple markers share one requirement.
    for x, y in [(825, 132), (520, 520), (2185, 248), (2250, 885)]:
        marker(draw, x, y, "M12", COLORS["curtain"])

    # Explicit non-scope items.
    draw.line((1005, 700, 1055, 750), fill=COLORS["skip"], width=5)
    draw.line((1055, 700, 1005, 750), fill=COLORS["skip"], width=5)
    draw.line((1010, 865, 1060, 915), fill=COLORS["skip"], width=5)
    draw.line((1060, 865, 1010, 915), fill=COLORS["skip"], width=5)

    if detailed:
        note_box(draw, 355, 440, "M5 书房桌位：2网口 + 工作站插座", COLORS["network"], target=(650, 520))
        note_box(draw, 900, 260, "M6 次卧/儿童房桌位：2网口 + 插座", COLORS["network"], target=(1130, 350))
        note_box(draw, 1970, 155, "M7 主卧阳台桌位：至少1网口 + 插座", COLORS["network"], target=(2125, 255))
        note_box(draw, 970, 545, "M3a AP1：走廊顶面 PoE 网线", COLORS["network"], target=(1255, 610))
        note_box(draw, 1985, 650, "M3b AP2：客厅顶面 PoE 网线", COLORS["network"], target=(1900, 705))
        note_box(draw, 1660, 960, "M8 影音柜：首期1网口 + 多位插座", COLORS["network"], target=(1860, 900))
        note_box(draw, 2055, 930, "M9 投影电源 + 影音管；幕布盒只220V", COLORS["power"], target=(2038, 860))
        note_box(draw, 1288, 770, "M1 衣帽间机柜/UPS/交换机/弱电汇聚", COLORS["power"], max_width=330, target=(1265, 840))
        note_box(draw, 850, 955, "M2 P2S 独立插座；不接机柜UPS/PDU", COLORS["power"], max_width=350, target=(1120, 910))
        note_box(draw, 1510, 360, "M10 设备侧：RS-485接入点候选", COLORS["rs485"], target=(1535, 425))
        note_box(draw, 1515, 515, "M11a 次卫洗衣：防潮插座/排水/水浸低位", COLORS["water"], max_width=360, target=(1455, 505))
        note_box(draw, 420, 920, "M11b 厨下净水/总水阀：插座和检修空间", COLORS["water"], max_width=350, target=(655, 832))
        note_box(draw, 2300, 790, "M12 窗帘盒：电机侧220V常电，单层窗帘", COLORS["curtain"], max_width=350, target=(2250, 885))
        note_box(draw, 1015, 660, "入户摄像头/门铃不做\nP2S不留墙网口", COLORS["skip"], max_width=250)


def draw_simple_overlays(draw: ImageDraw.ImageDraw) -> None:
    draw.rounded_rectangle((1040, 760, 1355, 1005), radius=14, outline=COLORS["power"], width=4)
    draw.rounded_rectangle((1585, 760, 2110, 985), radius=14, outline=COLORS["network"], width=4)


def footer(draw: ImageDraw.ImageDraw, h: int, simple: bool) -> None:
    text = (
        "说明：编号为业主额外要求/确认项；位置为示意，正式施工图由设计师按梁位、吊顶、柜体、家具和规范微调。"
        if simple
        else "说明：本图只标注业主需要设计师/装修队额外确认的必要项；普通插座、开关、灯具按设计师原图和电工规范执行。"
    )
    draw_box(draw, (40, h - 80, 1600, h - 28), outline="#999999", fill="white", width=1, radius=8)
    draw.text((60, h - 66), text, font=F_SMALL, fill=COLORS["ink"])


def render(simple: bool) -> Image.Image:
    base = Image.open(BASE).convert("RGB")
    side_w = 650
    canvas = Image.new("RGB", (base.width + side_w, base.height), "white")
    canvas.paste(base, (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw_title(draw, simple=simple)
    if simple:
        draw_simple_overlays(draw)
    draw_common_markers(draw, detailed=not simple)
    draw_side_panel(draw, base.width, base.height, simple=simple)
    footer(draw, base.height, simple=simple)
    return canvas


def main() -> None:
    OUT_DETAIL.parent.mkdir(parents=True, exist_ok=True)
    render(simple=False).save(OUT_DETAIL)
    render(simple=True).save(OUT_SIMPLE)
    print(f"wrote {OUT_DETAIL}")
    print(f"wrote {OUT_SIMPLE}")


if __name__ == "__main__":
    main()
