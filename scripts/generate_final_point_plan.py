#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "references/designer-input/强弱电点位图-original.png"
OUT = ROOT / "diagrams/14_强弱电与智能点位图_最终整合复核稿.png"
OUT_STORAGE = ROOT / "diagrams/15_衣帽间设备与插座点位_局部放大图.png"

FONT_CANDIDATES = [
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]

COLORS = {
    "power": "#e66a1f",
    "network": "#1769c2",
    "rs485": "#7351b8",
    "water": "#c73546",
    "curtain": "#16845a",
    "storage": "#b34b8c",
    "check": "#b77900",
    "ink": "#202124",
    "muted": "#5f6368",
    "panel": "#f7f8fa",
}


def font(size: int) -> ImageFont.FreeTypeFont:
    for candidate in FONT_CANDIDATES:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


F_TITLE = font(42)
F_SUB = font(23)
F_HEAD = font(30)
F_BODY = font(24)
F_SMALL = font(20)
F_TINY = font(17)
F_MARK = font(19)
F_MARK_TINY = font(15)


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont, width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        trial = current + char
        if not current or text_size(draw, trial, fnt)[0] <= width:
            current = trial
        else:
            lines.append(current)
            current = char
    if current:
        lines.append(current)
    return lines


def rounded_box(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    *,
    fill: str = "white",
    outline: str = "#777777",
    width: int = 2,
    radius: int = 10,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def marker(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    label: str,
    color: str,
    *,
    radius: int = 25,
) -> None:
    draw.ellipse(
        (x - radius, y - radius, x + radius, y + radius),
        fill=color,
        outline="white",
        width=4,
    )
    fnt = F_MARK_TINY if len(label) >= 4 else F_MARK
    tw, th = text_size(draw, label, fnt)
    draw.text((x - tw / 2, y - th / 2 - 1), label, font=fnt, fill="white")


def socket_group(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[int, int]],
    label: str,
    label_xy: tuple[int, int],
) -> None:
    for x, y in points:
        draw.ellipse((x - 13, y - 13, x + 13, y + 13), fill=COLORS["power"], outline="white", width=3)
    draw.text(label_xy, label, font=F_SMALL, fill=COLORS["power"])


def label_box(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    text: str,
    color: str,
    target: tuple[int, int],
    max_width: int = 350,
) -> None:
    lines = wrap(draw, text, F_SMALL, max_width)
    box_w = min(max_width + 24, max(text_size(draw, line, F_SMALL)[0] for line in lines) + 28)
    box_h = 18 + len(lines) * 25
    rounded_box(draw, (x, y, x + box_w, y + box_h), outline=color, width=2, radius=8)
    for idx, line in enumerate(lines):
        draw.text((x + 12, y + 8 + idx * 25), line, font=F_SMALL, fill=COLORS["ink"])
    tx, ty = target
    anchor_x = x if tx < x else x + box_w
    draw.line((anchor_x, y + box_h // 2, tx, ty), fill=color, width=3)


def draw_title(draw: ImageDraw.ImageDraw) -> None:
    # 标题移到右侧说明栏，避免遮住次卧顶墙点位。
    return


def draw_plan_markers(draw: ImageDraw.ImageDraw) -> None:
    # 衣帽间：主图只示意整体设备带，具体布置见右侧放大图。
    draw.rounded_rectangle((1035, 755, 1355, 1008), radius=12, outline=COLORS["storage"], width=5)
    marker(draw, 1258, 842, "S1", COLORS["storage"])
    label_box(
        draw,
        895,
        1015,
        "S1 衣帽间设备带：机柜、P2S、吸尘器、备用插座",
        COLORS["storage"],
        (1258, 842),
        max_width=420,
    )

    # 网络与 PoE。
    for x, y, label in [
        (1255, 610, "N1"),
        (1900, 705, "N2"),
        (1485, 620, "ZB"),
        (650, 520, "D1"),
        (1130, 350, "D2"),
        (2160, 245, "D3"),
        (1860, 900, "AV"),
    ]:
        marker(draw, x, y, label, COLORS["network"])

    # 短焦投影、电动幕布与影音柜，不做顶面投影电源。
    marker(draw, 2038, 860, "PJ", COLORS["power"])

    # RS-485 只标两端，不画可能被误认成实际路径的斜线。
    marker(draw, 1220, 802, "485", COLORS["rs485"], radius=28)
    marker(draw, 1660, 560, "485", COLORS["rs485"], radius=28)

    # 次卫 4 个用途点：B2 位于湿区马桶上方，其余按洗烘、扫地机和吹风机用途落位。
    for x, y, label in [
        (1495, 350, "B1"),
        (1455, 275, "B2"),
        (1495, 465, "B3"),
        (1560, 500, "B4"),
    ]:
        marker(draw, x, y, label, COLORS["power"], radius=20)

    # 厨下/总水阀检查点。
    marker(draw, 655, 832, "W2", COLORS["water"], radius=28)

    # 四组窗帘电机电源点：书房、次卧、主卧阳台、客厅阳台。
    for x, y, label in [
        (520, 300, "C1"),
        (1120, 100, "C2"),
        (2350, 355, "C3"),
        (2250, 885, "C4"),
    ]:
        marker(draw, x, y, label, COLORS["curtain"])

    # 补充纸图确认的普通插座。
    marker(draw, 1110, 520, "P1", COLORS["power"], radius=23)
    socket_group(draw, [(2285, 302), (2325, 302)], "P2 主卧阳台×2", (2180, 325))
    socket_group(
        draw,
        [(1388, 810), (1388, 855), (1388, 900)],
        "P3 共3个",
        (1415, 830),
    )

    # 全屋智能开关条件不逐点遮盖原图，统一在侧栏锁定。
    label_box(
        draw,
        1510,
        1030,
        "SW 全屋开关盒：零线 + 加深86底盒；关键照明保留本地手动",
        COLORS["check"],
        (1740, 910),
        max_width=450,
    )


def draw_bullet(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    label: str,
    text: str,
    color: str,
    width: int,
) -> int:
    marker(draw, x + 22, y + 18, label, color, radius=20)
    lines = wrap(draw, text, F_BODY, width - 62)
    for idx, line in enumerate(lines):
        draw.text((x + 58, y + idx * 29), line, font=F_BODY, fill=COLORS["ink"])
    return y + max(45, len(lines) * 29 + 10)


def draw_storage_inset(draw: ImageDraw.ImageDraw, x: int, y: int) -> int:
    draw.text((x, y), "衣帽间局部定案（约 1800 × 1726）", font=F_HEAD, fill=COLORS["ink"])
    y += 48

    # 以 1800 x 1726 的设计尺寸做比例示意。
    room_x, room_y = x + 18, y
    room_w, room_h = 570, 425
    draw.rectangle(
        (room_x, room_y, room_x + room_w, room_y + room_h),
        fill="white",
        outline="#222222",
        width=4,
    )

    # 门洞在左上，保留开启及进出设备空间。
    draw.line((room_x, room_y, room_x + 170, room_y), fill="white", width=8)
    draw.arc((room_x, room_y, room_x + 220, room_y + 220), 270, 360, fill="#777777", width=2)
    draw.line((room_x, room_y, room_x + 215, room_y + 28), fill="#777777", width=2)
    draw.text((room_x + 40, room_y + 20), "入口", font=F_TINY, fill=COLORS["muted"])

    # 保留左下部分衣柜；原右侧整排和右下角柜体改为设备带。
    wardrobe_w, wardrobe_h = 320, 135
    draw.rectangle(
        (room_x, room_y + room_h - wardrobe_h, room_x + wardrobe_w, room_y + room_h),
        fill="#e8eaed",
        outline="#8a8a8a",
        width=2,
    )
    draw.text((room_x + 86, room_y + room_h - 86), "保留衣柜", font=F_BODY, fill=COLORS["ink"])

    equipment_x = room_x + 345
    rack_h = 165
    printer_h = 185
    draw.rectangle(
        (equipment_x, room_y, room_x + room_w, room_y + rack_h),
        fill="#f2e5ee",
        outline=COLORS["storage"],
        width=3,
    )
    draw.text((equipment_x + 32, room_y + 35), "落地机柜", font=F_BODY, fill=COLORS["ink"])
    draw.text((equipment_x + 25, room_y + 70), "约600×600", font=F_SMALL, fill=COLORS["muted"])
    draw.text((equipment_x + 22, room_y + 108), "S1A 机柜电源", font=F_SMALL, fill=COLORS["power"])

    printer_y = room_y + rack_h + 10
    draw.rectangle(
        (equipment_x, printer_y, room_x + room_w, printer_y + printer_h),
        fill="#fae9dc",
        outline=COLORS["power"],
        width=3,
    )
    draw.text((equipment_x + 34, printer_y + 28), "P2S 独立台", font=F_BODY, fill=COLORS["ink"])
    draw.text((equipment_x + 20, printer_y + 63), "建议≥650×650", font=F_SMALL, fill=COLORS["muted"])
    draw.text((equipment_x + 18, printer_y + 99), "S1B 独立插座", font=F_SMALL, fill=COLORS["power"])
    draw.text((equipment_x + 18, printer_y + 130), "不接UPS/PDU", font=F_SMALL, fill=COLORS["muted"])

    # 低位清洁充电和高功率备用点，均与机柜、P2S 分开。
    draw.ellipse((room_x + 22, room_y + 215, room_x + 56, room_y + 249), fill=COLORS["power"])
    draw.text((room_x + 66, room_y + 216), "S1C 吸尘器充电", font=F_SMALL, fill=COLORS["ink"])
    draw.ellipse((room_x + 22, room_y + 256, room_x + 56, room_y + 290), fill=COLORS["power"])
    draw.text((room_x + 66, room_y + 257), "S1D 带地备用插座", font=F_SMALL, fill=COLORS["ink"])

    draw.text(
        (room_x + 18, room_y + room_h + 12),
        "取消原右侧整排柜体及右下角冲突柜体；设备前方保持可检修通道。",
        font=F_TINY,
        fill=COLORS["storage"],
    )
    return room_y + room_h + 48


def draw_side_panel(draw: ImageDraw.ImageDraw, start_x: int, height: int) -> None:
    panel_x = start_x + 20
    panel_w = 900
    rounded_box(
        draw,
        (panel_x, 28, panel_x + panel_w, height - 30),
        fill=COLORS["panel"],
        outline="#666666",
        width=2,
        radius=14,
    )
    x = panel_x + 36
    y = 52
    draw.text((x, y), "强弱电与智能点位图 - 最终整合复核稿", font=F_HEAD, fill=COLORS["ink"])
    draw.text((x, y + 38), "不遮盖原图；全部新增点位按编号计数", font=F_SMALL, fill=COLORS["muted"])
    y += 82
    draw.text((x, y), "全屋需要锁定", font=F_HEAD, fill=COLORS["ink"])
    y += 50

    items = [
        ("N1", "AP1：左侧中央走廊顶面，1 根 Cat6A PoE 回衣帽间", COLORS["network"]),
        ("N2", "AP2：客厅顶面，1 根 Cat6A PoE 回衣帽间", COLORS["network"]),
        ("ZB", "PoE Zigbee：中央开放高位，1 根 Cat6A 回衣帽间", COLORS["network"]),
        ("D1", "书房同一桌位：双口面板，2 根 Cat6A；3090 主位", COLORS["network"]),
        ("D2", "次卧桌位：双口面板，2 根 Cat6A + 桌面插座组", COLORS["network"]),
        ("D3", "主卧阳台桌位：1 根 Cat6A + 桌面插座组", COLORS["network"]),
        ("AV", "影音柜：1 根 Cat6A、多位插座、到投影/幕布的可抽换管", COLORS["network"]),
        ("PJ", "短焦投影在影音位；不留顶面投影电源；幕布盒留220V", COLORS["power"]),
        ("485", "日立与加湿各自独立管线回衣帽间；图中只标两端", COLORS["rs485"]),
        ("B1", "次卫4插座：B1洗烘、B2湿区马桶上方壁挂洗衣机、B3扫地机、B4吹风机", COLORS["power"]),
        ("W2", "厨下/总水阀：可检修插座、阀门空间、水浸落点", COLORS["water"]),
        ("C1", "C1书房、C2次卧、C3主卧阳台、C4客厅阳台：电机侧220V", COLORS["curtain"]),
        ("P1", "过道靠次卧墙面：新增1个普通带地插座", COLORS["power"]),
        ("P2", "主卧阳台靠C3位置：2个地插类/低位带地插座", COLORS["power"]),
        ("P3", "客餐厅靠衣帽间竖墙：由2个改为3个；水平墙原2个不变", COLORS["power"]),
    ]
    for label, text, color in items:
        y = draw_bullet(draw, x, y, label, text, color, panel_w - 72)

    y += 2
    rounded_box(
        draw,
        (x, y, panel_x + panel_w - 34, y + 77),
        fill="#fff8e5",
        outline=COLORS["check"],
        width=2,
        radius=8,
    )
    draw.text((x + 18, y + 10), "SW 全屋开关盒统一：零线 + 加深86底盒；不同回路零线不混用。", font=F_SMALL, fill=COLORS["ink"])
    draw.text(
        (x + 18, y + 40),
        "纸图蓝色普通开关/插座修改须由设计师逐点转入CAD。",
        font=F_SMALL,
        fill=COLORS["ink"],
    )
    y += 96
    rounded_box(
        draw,
        (x, y + 5, panel_x + panel_w - 34, y + 155),
        fill="white",
        outline=COLORS["storage"],
        width=2,
        radius=8,
    )
    draw.text((x + 18, y + 18), "衣帽间设备带详见图15", font=F_HEAD, fill=COLORS["storage"])
    storage_lines = [
        "S1A 机柜/UPS输入；S1B P2S独立插座；S1C 吸尘器；S1D 备用。",
        "取消原右侧整排柜体和右下角冲突柜体；P2S不单留墙面网口。",
        "3090主位仍在书房；机柜和P2S不做密闭柜。",
    ]
    sy = y + 62
    for line in storage_lines:
        draw.text((x + 18, sy), line, font=F_SMALL, fill=COLORS["ink"])
        sy += 29


def draw_footer(draw: ImageDraw.ImageDraw, height: int) -> None:
    rounded_box(draw, (36, height - 78, 2040, height - 26), outline="#999999", width=1, radius=8)
    draw.text(
        (56, height - 64),
        "说明：本图锁定功能和施工条件；精确尺寸、高度、柜体收口、吊顶避让及纸图蓝字由设计师在正式CAD施工图中标注。",
        font=F_SMALL,
        fill=COLORS["ink"],
    )


def render_storage_detail() -> Image.Image:
    canvas = Image.new("RGB", (1800, 1160), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((60, 38), "衣帽间设备与插座点位 - 局部放大图", font=font(48), fill=COLORS["ink"])
    draw.text(
        (62, 96),
        "按平面图标注约 1800 × 1726；最终净尺寸、门套、柜体和设备尺寸由设计师现场复核",
        font=F_BODY,
        fill=COLORS["muted"],
    )

    room_x, room_y = 70, 185
    room_w, room_h = 860, 820
    draw.rectangle(
        (room_x, room_y, room_x + room_w, room_y + room_h),
        fill="#ffffff",
        outline="#222222",
        width=5,
    )
    draw.line((room_x, room_y, room_x + 255, room_y), fill="white", width=10)
    draw.arc((room_x, room_y, room_x + 330, room_y + 330), 270, 360, fill="#777777", width=3)
    draw.line((room_x, room_y, room_x + 322, room_y + 35), fill="#777777", width=3)
    draw.text((room_x + 54, room_y + 35), "入口", font=F_BODY, fill=COLORS["muted"])

    # 右侧为连续设备带；左下仅保留不冲突的衣柜。
    equipment_x = room_x + 550
    equipment_w = room_w - 550
    rack_h = 305
    printer_y = room_y + rack_h + 18
    printer_h = 350
    wardrobe_h = 270

    draw.rectangle(
        (equipment_x, room_y, room_x + room_w, room_y + rack_h),
        fill="#f2e5ee",
        outline=COLORS["storage"],
        width=4,
    )
    draw.text((equipment_x + 62, room_y + 62), "落地机柜", font=F_HEAD, fill=COLORS["ink"])
    draw.text((equipment_x + 45, room_y + 108), "预留约650×650", font=F_BODY, fill=COLORS["muted"])
    draw.text((equipment_x + 42, room_y + 166), "S1A 机柜/UPS输入", font=F_BODY, fill=COLORS["power"])
    draw.text((equipment_x + 42, room_y + 208), "光纤、Cat6A、RS-485", font=F_SMALL, fill=COLORS["network"])
    draw.text((equipment_x + 42, room_y + 240), "集中到配线架", font=F_SMALL, fill=COLORS["network"])

    draw.rectangle(
        (equipment_x, printer_y, room_x + room_w, printer_y + printer_h),
        fill="#fae9dc",
        outline=COLORS["power"],
        width=4,
    )
    draw.text((equipment_x + 58, printer_y + 50), "P2S 独立台", font=F_HEAD, fill=COLORS["ink"])
    draw.text((equipment_x + 38, printer_y + 98), "台面建议≥650×650", font=F_BODY, fill=COLORS["muted"])
    draw.text((equipment_x + 40, printer_y + 157), "S1B 独立带地插座", font=F_BODY, fill=COLORS["power"])
    draw.text((equipment_x + 40, printer_y + 201), "不接机柜UPS/PDU", font=F_BODY, fill=COLORS["muted"])
    draw.text((equipment_x + 40, printer_y + 245), "不单留墙面网口", font=F_BODY, fill=COLORS["muted"])
    draw.text((equipment_x + 40, printer_y + 289), "前方留开门/维护空间", font=F_SMALL, fill=COLORS["muted"])

    draw.rectangle(
        (room_x, room_y + room_h - wardrobe_h, equipment_x - 18, room_y + room_h),
        fill="#e8eaed",
        outline="#8a8a8a",
        width=3,
    )
    draw.text((room_x + 170, room_y + room_h - 152), "保留衣柜", font=F_HEAD, fill=COLORS["ink"])
    draw.text((room_x + 96, room_y + room_h - 101), "右下角与设备带冲突部分取消", font=F_SMALL, fill=COLORS["muted"])

    # 两个独立低位插座设在左侧可检修墙面。
    for cy, label in [
        (room_y + 490, "S1C 吸尘器充电插座"),
        (room_y + 555, "S1D 带地备用插座"),
    ]:
        draw.ellipse((room_x + 34, cy - 20, room_x + 74, cy + 20), fill=COLORS["power"])
        draw.text((room_x + 92, cy - 17), label, font=F_BODY, fill=COLORS["ink"])

    draw.line(
        (room_x + 295, room_y + 365, equipment_x - 35, room_y + 365),
        fill=COLORS["storage"],
        width=3,
    )
    draw.polygon(
        [
            (equipment_x - 35, room_y + 365),
            (equipment_x - 53, room_y + 355),
            (equipment_x - 53, room_y + 375),
        ],
        fill=COLORS["storage"],
    )
    draw.text((room_x + 300, room_y + 320), "设备前检修通道建议≥800", font=F_SMALL, fill=COLORS["storage"])

    panel_x = 995
    rounded_box(
        draw,
        (panel_x, 175, 1740, 1040),
        fill=COLORS["panel"],
        outline="#666666",
        width=2,
        radius=14,
    )
    draw.text((panel_x + 34, 205), "施工锁定项", font=F_HEAD, fill=COLORS["ink"])
    notes = [
        ("1", "取消原图右侧整排柜体，并取消右下角与 P2S 台冲突的柜体。"),
        ("2", "S1A：1 组独立带地墙插，作为 UPS 输入；UPS 后接机柜 PDU。"),
        ("3", "S1B：P2S/AMS 独立带地插座，建议放在台面上方或侧方可插拔处。"),
        ("4", "S1C：吸尘器充电普通墙插；S1D：带地备用墙插，均不接 UPS。"),
        ("5", "3090 工作站主位仍在书房；S1D 只作备用，启用高功率负载前复核回路。"),
        ("6", "所有入户光纤、各房 Cat6A、两路 RS-485 回到机柜配线架/网关侧。"),
        ("7", "P2S 首期用 Wi-Fi；如需有线，直接接机柜交换机，不做墙面网口。"),
        ("8", "机柜和 P2S 不做密闭柜；门下留回风条件，可选排风路线现场确认。"),
        ("9", "若现场净宽不能保证约 800 mm 检修通道，优先继续减少衣柜，不压缩设备维护空间。"),
    ]
    y = 265
    for idx, note in notes:
        draw.ellipse((panel_x + 38, y + 4, panel_x + 72, y + 38), fill=COLORS["storage"])
        tw, th = text_size(draw, idx, F_SMALL)
        draw.text((panel_x + 55 - tw / 2, y + 20 - th / 2), idx, font=F_SMALL, fill="white")
        lines = wrap(draw, note, F_BODY, 610)
        for line_idx, line in enumerate(lines):
            draw.text((panel_x + 90, y + line_idx * 31), line, font=F_BODY, fill=COLORS["ink"])
        y += max(58, len(lines) * 31 + 16)

    rounded_box(
        draw,
        (60, 1060, 1740, 1125),
        fill="#fff8e5",
        outline=COLORS["check"],
        width=2,
        radius=8,
    )
    draw.text(
        (82, 1078),
        "本图先锁定功能分区和施工条件；插座高度、回路、柜体板厚、散热开口及设备实际尺寸由设计师和电工复核后标入CAD。",
        font=F_BODY,
        fill=COLORS["ink"],
    )
    return canvas


def main() -> None:
    base = Image.open(BASE).convert("RGB")
    side_w = 950
    canvas = Image.new("RGB", (base.width + side_w, base.height), "white")
    canvas.paste(base, (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw_title(draw)
    draw_plan_markers(draw)
    draw_side_panel(draw, base.width, base.height)
    draw_footer(draw, base.height)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT)
    render_storage_detail().save(OUT_STORAGE)
    print(f"wrote {OUT}")
    print(f"wrote {OUT_STORAGE}")


if __name__ == "__main__":
    main()
