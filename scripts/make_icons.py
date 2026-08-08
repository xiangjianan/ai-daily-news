#!/usr/bin/env python3
"""
AI 科技日报 - 应用图标生成器

设计方向：「AI 报头印章」
  墨黑底 + 奶白纸卡(双线报纸边框) + 黑色报头条内嵌奶白粗衬线 "AI"
  + 棕褐报纸文字栏 + 左下出版红点

输出（项目根 icons/）：
  icon-512.png / icon-192.png      —— 标准（purpose=any）
  maskable-512.png                 —— maskable（内容收进中心安全区）
  apple-touch-icon.png (180)       —— iOS
  favicon-32.png                   —— 浏览器标签
  icon.svg                         —— 矢量（favicon + manifest any）

可复跑：python3 scripts/make_icons.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

# 品牌色（与 assets/style.css 一致）
INK = (26, 26, 26)          # #1a1a1a 墨黑
CREAM = (255, 254, 248)     # #fffef8 奶白纸
SEPIA = (139, 90, 43)       # #8b5a2b 棕褐
BRICK = (192, 57, 43)       # 出版红点

GEORGIA_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"


def _font(size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(GEORGIA_BOLD, size)
    except Exception:
        return ImageFont.load_default()


def draw_icon(size: int, maskable: bool = False) -> Image.Image:
    """绘制单枚图标。maskable=True 时把纸卡收小，确保关键内容在中心 80% 安全区。"""
    s = float(size)
    img = Image.new("RGB", (size, size), INK)
    d = ImageDraw.Draw(img)

    # 奶白纸卡（居中圆角）
    card_frac = 0.60 if maskable else 0.80
    m = s * (1 - card_frac) / 2
    radius = int(s * 0.11)
    d.rounded_rectangle([m, m, s - m, s - m], radius=radius, fill=CREAM)

    # 内容内边距
    p = m + s * 0.055
    right = bottom = s - p
    content_w = right - p

    # 双线报纸边框
    bw = max(2, round(s * 0.013))
    d.rounded_rectangle([p, p, s - p, s - p],
                        radius=max(3, radius - round(s * 0.04)), outline=INK, width=bw)
    p2 = p + bw * 2.4
    d.rounded_rectangle([p2, p2, s - p2, s - p2],
                        radius=max(3, radius - round(s * 0.07)), outline=INK, width=bw)

    # 黑色报头条
    bar_x1, bar_x2 = p2, s - p2
    bar_y1 = p2 + content_w * 0.04
    bar_h = content_w * 0.30
    bar_y2 = bar_y1 + bar_h
    d.rectangle([bar_x1, bar_y1, bar_x2, bar_y2], fill=INK)

    # 奶白粗衬线 "AI"（垂直水平居中于报头条）
    font = _font(int(bar_h * 0.62))
    bbox = d.textbbox((0, 0), "AI", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((s - tw) / 2 - bbox[0], (bar_y1 + bar_y2 - th) / 2 - bbox[1]),
           "AI", font=font, fill=CREAM)

    # 棕褐报纸文字栏（3 条，长短错落）
    rules_top = bar_y2 + content_w * 0.11
    rules_bot = bottom - content_w * 0.10
    slot = (rules_bot - rules_top) / 3
    lh = max(2, round(s * 0.022))
    for i, wf in enumerate((0.96, 0.70, 0.86)):
        cy = rules_top + slot * i + slot * 0.5
        rw = (bar_x2 - p2) * wf
        d.rounded_rectangle([p2, cy - lh / 2, p2 + rw, cy + lh / 2],
                            radius=max(1, lh // 2), fill=SEPIA)

    # 左下出版红点
    dr = max(3, round(s * 0.024))
    cx = p2 + dr
    cy = bottom - dr
    d.ellipse([cx - dr, cy - dr, cx + dr, cy + dr], fill=BRICK)

    return img


SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="AI 科技日报">
  <rect width="512" height="512" fill="#1a1a1a"/>
  <rect x="51" y="51" width="410" height="410" rx="56" fill="#fffef8"/>
  <rect x="79" y="79" width="354" height="354" rx="40" fill="none" stroke="#1a1a1a" stroke-width="7"/>
  <rect x="96" y="96" width="320" height="320" rx="28" fill="none" stroke="#1a1a1a" stroke-width="7"/>
  <rect x="110" y="110" width="292" height="106" fill="#1a1a1a"/>
  <text x="256" y="163" text-anchor="middle" dominant-baseline="central"
        font-family="Georgia, 'Times New Roman', serif" font-weight="bold"
        font-size="66" fill="#fffef8" letter-spacing="4">AI</text>
  <rect x="96" y="251" width="307" height="11" rx="5" fill="#8b5a2b"/>
  <rect x="96" y="320" width="224" height="11" rx="5" fill="#8b5a2b"/>
  <rect x="96" y="389" width="275" height="11" rx="5" fill="#8b5a2b"/>
  <circle cx="100" cy="429" r="12" fill="#c0392b"/>
</svg>
"""


def main() -> None:
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(project_dir, "icons")
    os.makedirs(out_dir, exist_ok=True)

    def save(img: Image.Image, name: str, sz: int) -> None:
        path = os.path.join(out_dir, name)
        img.resize((sz, sz), Image.LANCZOS).save(path, "PNG")
        print(f"✓ {name} ({sz}×{sz})")

    master_any = draw_icon(512, maskable=False)
    master_mask = draw_icon(512, maskable=True)

    save(master_any, "icon-512.png", 512)
    save(master_any, "icon-192.png", 192)
    save(master_any, "apple-touch-icon.png", 180)
    save(master_any, "favicon-32.png", 32)
    master_mask.resize((512, 512), Image.LANCZOS).save(os.path.join(out_dir, "maskable-512.png"), "PNG")
    print("✓ maskable-512.png (512×512)")

    with open(os.path.join(out_dir, "icon.svg"), "w", encoding="utf-8") as f:
        f.write(SVG)
    print("✓ icon.svg")

    print(f"\n✓ 图标已生成于 {out_dir}")


if __name__ == "__main__":
    main()
