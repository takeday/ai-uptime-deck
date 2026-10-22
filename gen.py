"""Generate intro manga SVGs for the Marp deck."""
import math
import os
import random
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
FONT = "'Hiragino Maru Gothic ProN','Hiragino Sans','Noto Sans JP','Yu Gothic','Meiryo',sans-serif"
INK = "#222"
SKIN = "#ffe0c7"
HAIR = "#2d2a32"
SHIRT = "#3f72d9"
AI_FILL = "#e8f1ff"
AI_STROKE = "#3b6fd8"
ACCENT = "#e8483b"


def t(x, y, s, size, anchor="middle", weight="700", fill=INK, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" '
            f'font-weight="{weight}" fill="{fill}" {extra}>{s}</text>')


def ml(cx, cy, lines, size, lh=1.3, **kw):
    total = (len(lines) - 1) * size * lh
    y0 = cy - total / 2 + size * 0.36
    return "".join(t(cx, y0 + i * size * lh, l, size, **kw) for i, l in enumerate(lines))


def poly(pts, fill, stroke=None, sw=3):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    st = f'stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else 'stroke="none"'
    return f'<polygon points="{p}" fill="{fill}" {st}/>'


def ebubble(cx, cy, rx, ry, tip, lines, size, fill="#fff", stroke=INK, tcolor=INK):
    a = math.atan2((tip[1] - cy) / ry, (tip[0] - cx) / rx)
    d = 0.2
    pt = lambda ang, k=1.0: (cx + rx * k * math.cos(ang), cy + ry * k * math.sin(ang))
    p1, p2 = pt(a - d), pt(a + d)
    q1, q2 = pt(a - d * 0.8, 0.9), pt(a + d * 0.8, 0.9)
    mid = pt(a)
    inner = (mid[0] + 0.3 * (tip[0] - mid[0]), mid[1] + 0.3 * (tip[1] - mid[1]))
    return (poly([p1, tip, p2], fill, stroke)
            + f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + poly([q1, inner, q2], fill)
            + ml(cx, cy, lines, size, fill=tcolor))


def rbubble(x, y, w, h, tip, lines, size, fill=AI_FILL, stroke=AI_STROKE, tcolor=INK, anchor="middle"):
    cx, cy = x + w / 2, y + h / 2
    if tip[0] < x:
        b1, b2, c1, c2 = (x, cy - 10), (x, cy + 10), (x + 5, cy - 7), (x + 5, cy + 7)
    elif tip[0] > x + w:
        b1, b2, c1, c2 = (x + w, cy - 10), (x + w, cy + 10), (x + w - 5, cy - 7), (x + w - 5, cy + 7)
    elif tip[1] > y + h:
        bx = min(max(tip[0], x + 24), x + w - 24)
        b1, b2, c1, c2 = (bx - 12, y + h), (bx + 12, y + h), (bx - 9, y + h - 5), (bx + 9, y + h - 5)
    else:
        bx = min(max(tip[0], x + 24), x + w - 24)
        b1, b2, c1, c2 = (bx - 12, y), (bx + 12, y), (bx - 9, y + 5), (bx + 9, y + 5)
    mid = ((b1[0] + b2[0]) / 2, (b1[1] + b2[1]) / 2)
    inner = (mid[0] + 0.3 * (tip[0] - mid[0]), mid[1] + 0.3 * (tip[1] - mid[1]))
    tx = cx if anchor == "middle" else x + 16
    return (poly([b1, tip, b2], fill, stroke)
            + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            + poly([c1, inner, c2], fill)
            + ml(tx, cy, lines, size, fill=tcolor, anchor=anchor))


def burst(cx, cy, n, r1, r2, color, seed=1, wmax=5):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n + rnd.uniform(-0.04, 0.04)
        ra = r1 + rnd.uniform(0, 40)
        w = rnd.uniform(1.5, wmax)
        out.append(f'<line x1="{cx + ra * math.cos(a):.1f}" y1="{cy + ra * math.sin(a):.1f}" '
                   f'x2="{cx + r2 * math.cos(a):.1f}" y2="{cy + r2 * math.sin(a):.1f}" '
                   f'stroke="{color}" stroke-width="{w:.1f}" stroke-linecap="round"/>')
    return "".join(out)


# ---------- character ----------

def expr(kind):
    if kind == "determined":
        return ('<path d="M-30,-16 L-7,-8 M30,-16 L7,-8" stroke="#222" stroke-width="5" stroke-linecap="round"/>'
                '<ellipse cx="-16" cy="4" rx="5.5" ry="8.5" fill="#222"/><ellipse cx="16" cy="4" rx="5.5" ry="8.5" fill="#222"/>'
                '<circle cx="-14" cy="0" r="2.2" fill="#fff"/><circle cx="18" cy="0" r="2.2" fill="#fff"/>'
                '<path d="M-13,20 Q0,36 13,20 Z" fill="#fff" stroke="#222" stroke-width="3" stroke-linejoin="round"/>')
    if kind == "intense":
        return ('<path d="M-30,-14 L-7,-6 M30,-14 L7,-6" stroke="#222" stroke-width="5" stroke-linecap="round"/>'
                '<path d="M-24,4 L-8,4 M8,4 L24,4" stroke="#222" stroke-width="6" stroke-linecap="round"/>'
                '<path d="M-10,24 L10,24" stroke="#222" stroke-width="3.5" stroke-linecap="round"/>'
                + drop(54, -26) )
    if kind == "panic":
        return ('<path d="M-28,-10 L-8,-19 M28,-10 L8,-19" stroke="#222" stroke-width="4" stroke-linecap="round"/>'
                '<circle cx="-16" cy="5" r="8" fill="#fff" stroke="#222" stroke-width="2.5"/><circle cx="16" cy="5" r="8" fill="#fff" stroke="#222" stroke-width="2.5"/>'
                '<circle cx="-16" cy="5" r="2.6" fill="#222"/><circle cx="16" cy="5" r="2.6" fill="#222"/>'
                '<path d="M-12,26 q4,-6 8,0 q4,6 8,0 q4,-6 8,0" fill="none" stroke="#222" stroke-width="3" stroke-linecap="round"/>'
                + drop(54, -30) + drop(-58, -18, 0.8) + drop(60, 4, 0.7))
    if kind == "exhausted":
        return ('<circle r="46" fill="#cdbfe0" opacity="0.45"/>'
                '<path d="M-20,-44 L-20,-22 M-8,-46 L-8,-20 M4,-46 L4,-22 M16,-44 L16,-24" stroke="#7a62a8" stroke-width="2.5"/>'
                '<path d="M-26,4 Q-17,9 -8,4 M8,4 Q17,9 26,4" fill="none" stroke="#222" stroke-width="3.5" stroke-linecap="round"/>'
                '<path d="M-25,12 Q-17,16 -9,12 M9,12 Q17,16 25,12" fill="none" stroke="#8a7aa6" stroke-width="2.5" stroke-linecap="round"/>'
                '<ellipse cx="2" cy="27" rx="6" ry="7" fill="#5a3a3a" stroke="#222" stroke-width="2.5"/>')
    if kind == "happy":
        return ('<path d="M-27,-14 Q-17,-20 -7,-15 M27,-14 Q17,-20 7,-15" fill="none" stroke="#222" stroke-width="4" stroke-linecap="round"/>'
                '<path d="M-26,6 Q-17,-6 -8,6 M8,6 Q17,-6 26,6" fill="none" stroke="#222" stroke-width="4.5" stroke-linecap="round"/>'
                '<path d="M-15,17 Q0,40 15,17 Z" fill="#e8605a" stroke="#222" stroke-width="3" stroke-linejoin="round"/>'
                '<ellipse cx="-29" cy="16" rx="8" ry="5" fill="#ff8f8f" opacity="0.6"/><ellipse cx="29" cy="16" rx="8" ry="5" fill="#ff8f8f" opacity="0.6"/>')
    raise ValueError(kind)


def drop(x, y, s=1.0):
    return (f'<path transform="translate({x},{y}) scale({s})" d="M0,-12 C6,-2 9,4 9,8 A9,9 0 0 1 -9,8 C-9,4 -6,-2 0,-12 Z" '
            f'fill="#9fd3ff" stroke="#2c6fb3" stroke-width="2.5"/>')


def head(kind):
    return (f'<circle cx="-46" cy="6" r="9" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="46" cy="6" r="9" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>'
            f'<circle r="46" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M-49,4 C-56,-46 -20,-63 4,-61 C38,-59 57,-36 49,6 C44,-12 36,-22 26,-27 L20,-14 L10,-29 '
            f'C0,-20 -14,-20 -24,-31 C-30,-18 -40,-8 -49,4 Z" fill="{HAIR}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
            + expr(kind))


def torso(length=170, color=SHIRT):
    return (f'<path d="M-30,40 Q0,52 30,40 L62,78 Q72,92 72,{length} L-72,{length} Q-72,92 -62,78 Z" '
            f'fill="{color}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M-15,42 L0,60 L15,42" fill="#fff" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')


def arm(d, hand):
    hx, hy = hand
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="28" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{SHIRT}" stroke-width="22" stroke-linecap="round"/>'
            f'<circle cx="{hx}" cy="{hy}" r="16" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>')


def person(x, y, kind, arms="", tilt=0, length=170):
    return (f'<g transform="translate({x},{y})">{torso(length)}{arms}'
            f'<g transform="rotate({tilt})">{head(kind)}</g></g>')


def laptop_back(cx, top, w=200, h=110):
    x = cx - w / 2
    return (f'<rect x="{x - 14}" y="{top + h - 2}" width="{w + 28}" height="12" rx="4" fill="#b8c0cc" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{x}" y="{top}" width="{w}" height="{h}" rx="10" fill="#d9dfe8" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="{cx}" cy="{top + h / 2}" r="22" fill="#fff" stroke="{AI_STROKE}" stroke-width="3"/>'
            + t(cx, top + h / 2 + 7, "AI", 19, fill=AI_STROKE, weight="800"))


def desk(y, w, h=60, color="#c99a6b"):
    return f'<rect x="-10" y="{y}" width="{w + 20}" height="{h}" fill="{color}" stroke="{INK}" stroke-width="3"/>'


def badge(n):
    return (f'<circle cx="22" cy="22" r="15" fill="{INK}"/>' + t(22, 29, str(n), 18, fill="#fff", weight="800"))


def sfx(x, y, s, size, rot=-8, fill=ACCENT, stroke="#fff"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="900" text-anchor="middle" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="6" paint-order="stroke" transform="rotate({rot} {x} {y})">{s}</text>')


def paper(x, y, rot, label):
    return (f'<g transform="translate({x},{y}) rotate({rot})">'
            f'<rect x="-38" y="-18" width="76" height="36" rx="3" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
            + t(0, 6, label, 16) + '</g>')


def panel(x, y, w, h, body, bg="#fff"):
    return (f'<g transform="translate({x},{y})"><g clip-path="url(#clip{w}x{h})">'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>{body}</g>'
            f'<rect width="{w}" height="{h}" fill="none" stroke="{INK}" stroke-width="5"/></g>')


def svg(w, h, clips, body):
    cl = "".join(f'<clipPath id="clip{cw}x{ch}"><rect width="{cw}" height="{ch}"/></clipPath>' for cw, ch in clips)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}">'
            f'<defs>{cl}</defs><rect width="{w}" height="{h}" fill="#fbf8f1"/>{body}</svg>\n')


# ---------- page 1: the "AI babysitting" day ----------
PW, PH = 608, 328


def p1():
    cx, hy = 190, 122
    fist = arm("M56,84 Q96,50 86,-6", (88, -22))
    return (burst(cx, hy, 64, 120, 520, "#f2d98c", seed=3, wmax=7)
            + person(cx, hy, "determined", fist)
            + laptop_back(cx, hy + 64)
            + desk(hy + 184, PW)
            + sfx(70, 66, "キリッ", 30, rot=-12)
            + ebubble(450, 112, 142, 76, (290, 120), ["よし、AIに", "細かく指示出して", "確実に進めていくぞ！"], 23)
            + badge(1))


def p2():
    cx, hy = 170, 126
    hands = ""
    for sx in (-1, 1):
        hx = cx + sx * 116
        hands += (f'<circle cx="{hx}" cy="{hy + 104}" r="15" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>'
                  f'<path d="M{hx + sx * 22},{hy + 86} q{sx * 10},14 0,30 M{hx + sx * 32},{hy + 80} q{sx * 14},20 0,42" '
                  f'fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>')
    papers = "".join(paper(x, y, r, l) for x, y, r, l in [
        (352, 214, -14, "指示①"), (430, 262, 10, "指示②"), (506, 212, -6, "指示③"),
        (566, 276, 16, "指示④"), (366, 290, 6, "指示⑤"), (476, 300, -10, "指示⑥")])
    return (person(cx, hy, "intense")
            + laptop_back(cx, hy + 64)
            + hands
            + desk(hy + 184, PW)
            + papers
            + sfx(250, 58, "カタカタカタカタッ", 30, rot=-6)
            + ebubble(452, 96, 136, 62, (282, 130), ["どんどん指示を", "書いて行くぞ！"], 25)
            + badge(2))


def p3():
    cx, hy = 122, 150
    tip = (226, 236)
    qs = [["A案とB案、どちらにしますか？"], ["この場合の例外処理は？"],
          ["念のため確認させてください"], ["次は何をしますか？"]]
    bubbles = "".join(rbubble(282, 16 + i * 78, 308, 60, (262, 52 + i * 78), q, 19) for i, q in enumerate(qs))
    clock = ('<g transform="translate(40,46)"><circle r="25" fill="#fff" stroke="#222" stroke-width="3"/>'
             '<path d="M0,0 L0,-15 M0,0 L11,6" stroke="#222" stroke-width="3" stroke-linecap="round"/>'
             '<path d="M-34,-10 A36,36 0 0 1 -12,-34 M34,10 A36,36 0 0 1 12,34" fill="none" stroke="#888" stroke-width="2.5"/></g>')
    return (person(cx, hy, "panic")
            + laptop_back(cx, hy + 64)
            + desk(hy + 174, PW)
            + clock
            + ebubble(176, 50, 76, 32, (150, 92), ["え、えっと…"], 20)
            + bubbles
            + badge(3))


def p4():
    cx, hy = 300, 168
    window = ('<rect x="30" y="34" width="150" height="112" fill="#2c3a63" stroke="#0e1426" stroke-width="5"/>'
              '<path d="M105,34 L105,146 M30,90 L180,90" stroke="#0e1426" stroke-width="4"/>'
              '<circle cx="70" cy="64" r="16" fill="#f7e9a8"/><circle cx="77" cy="58" r="14" fill="#2c3a63"/>'
              '<circle cx="146" cy="56" r="2" fill="#fff"/><circle cx="160" cy="120" r="1.6" fill="#fff"/>'
              '<circle cx="48" cy="124" r="1.6" fill="#fff"/>')
    glow = f'<ellipse cx="{cx}" cy="{hy + 70}" rx="150" ry="120" fill="#7aa7ff" opacity="0.18"/>'
    soul = ('<g transform="translate(372,86) rotate(18)">'
            '<path d="M0,-26 C20,-26 28,-6 22,10 C18,22 6,26 -2,34 C-4,24 -20,22 -22,6 C-26,-12 -16,-26 0,-26 Z" '
            'fill="#fff" stroke="#9aa6c8" stroke-width="2.5" opacity="0.95"/>'
            '<circle cx="-6" cy="-6" r="2.5" fill="#555"/><circle cx="8" cy="-6" r="2.5" fill="#555"/></g>')
    limp = (f'<circle cx="{cx - 112}" cy="{hy + 140}" r="15" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="{cx + 112}" cy="{hy + 140}" r="15" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>')
    return (window + glow
            + person(cx, hy, "exhausted", tilt=-14)
            + soul
            + laptop_back(cx, hy + 62, h=92)
            + limp
            + desk(hy + 164, PW, color="#7d5c3e")
            + sfx(500, 62, "チーン…", 30, rot=-6, fill="#fff", stroke="#1f2a44")
            + ebubble(496, 180, 104, 62, (412, 196), ["…今日ずっと", "AIの相手しか", "してない…"], 19)
            + rbubble(20, 210, 158, 58, (198, 250), ["次のご指示を", "お待ちしています"], 15)
            + badge(4))


def page1():
    g = 16
    body = (panel(24, 24, PW, PH, p1())
            + panel(24 + PW + g, 24, PW, PH, p2())
            + panel(24, 24 + PH + g, PW, PH, p3())
            + panel(24 + PW + g, 24 + PH + g, PW, PH, p4(), bg="#1f2a44"))
    return svg(1280, 720, [(PW, PH)], body)


# ---------- page 2: the ideal ----------
BW, BH = 1200, 410


def big_panel():
    whiteboard = ('<rect x="40" y="96" width="330" height="200" rx="6" fill="#fff" stroke="#222" stroke-width="4"/>'
                  '<path d="M80,296 L64,380 M330,296 L346,380" stroke="#222" stroke-width="4"/>'
                  + t(205, 136, "次の一手", 26)
                  + '<polyline points="70,262 130,236 180,248 240,196 300,170" fill="none" stroke="#2fa36b" stroke-width="5" stroke-linejoin="round"/>'
                  '<polygon points="300,170 284,168 296,184" fill="#2fa36b" stroke="#2fa36b" stroke-width="4" stroke-linejoin="round"/>'
                  '<rect x="290" y="210" width="58" height="50" fill="#ffe57a" stroke="#222" stroke-width="2" transform="rotate(6 319 235)"/>'
                  + t(320, 242, "新企画", 14, extra='transform="rotate(6 319 235)"')
                  + '<g transform="translate(92,184)"><circle r="20" fill="#fff6b0" stroke="#222" stroke-width="3"/>'
                  '<rect x="-9" y="18" width="18" height="12" fill="#bbb" stroke="#222" stroke-width="2.5"/>'
                  '<path d="M-34,-10 L-26,-6 M34,-10 L26,-6 M0,-36 L0,-28 M-24,-30 L-18,-22 M24,-30 L18,-22" stroke="#e0a800" stroke-width="3" stroke-linecap="round"/></g>')
    colleagues = ""
    for x, c in ((150, "#6c8f5a"), (290, "#b5646d")):
        colleagues += (f'<g transform="translate({x},346)">'
                       f'<path d="M-66,110 Q-66,34 0,34 Q66,34 66,110 Z" fill="{c}" stroke="#222" stroke-width="3"/>'
                       f'<circle r="38" fill="{HAIR}" stroke="#222" stroke-width="3"/></g>')
    point = arm("M-56,84 Q-96,60 -126,30", (-132, 24))
    hero = person(470, 160, "happy", point, length=300)

    sep = '<path d="M640,0 L626,90 L652,170 L624,250 L650,330 L632,410" fill="none" stroke="#222" stroke-width="4" stroke-dasharray="14 10"/>'
    right_bg = '<rect x="640" y="0" width="560" height="410" fill="#eef4ff"/>'
    label = (f'<rect x="676" y="18" width="500" height="40" rx="20" fill="{AI_STROKE}"/>'
             + t(926, 45, "その間、AIはバックグラウンドで稼働中", 20, fill="#fff"))
    screen_lines = ["$ workflow run 一括チェック", "  ▶ 3 agents 実行中…", "$ /loop 30m 日次巡回", "  ✓ 新着PR 2件 確認済"]
    lap = ('<rect x="694" y="210" width="196" height="122" rx="10" fill="#3a4152" stroke="#222" stroke-width="3"/>'
           '<rect x="704" y="220" width="176" height="102" rx="4" fill="#1b2130"/>'
           + "".join(t(712, 242 + i * 22, s, 12, anchor="start", weight="600",
                       fill="#9ef0b8" if s.strip().startswith(("▶", "✓")) else "#e6edf7") for i, s in enumerate(screen_lines))
           + '<path d="M674,332 L910,332 L924,350 L660,350 Z" fill="#b8c0cc" stroke="#222" stroke-width="3" stroke-linejoin="round"/>')
    cards = [("✓", "#2fa36b", "セキュリティ検査"), ("✓", "#2fa36b", "文書の抜け漏れチェック"),
             ("▶", AI_STROKE, "PRレビュー"), ("▶", AI_STROKE, "/loop 日次巡回")]
    cardsvg = ""
    for i, (ic, col, lab) in enumerate(cards):
        y = 80 + i * 66
        cardsvg += (f'<rect x="920" y="{y}" width="262" height="52" rx="10" fill="#fff" stroke="#222" stroke-width="3"/>'
                    f'<circle cx="946" cy="{y + 26}" r="14" fill="{col}"/>'
                    + t(946, y + 32, ic, 17, fill="#fff", weight="800")
                    + t(970, y + 33, lab, 19, anchor="start"))
    ai_say = rbubble(680, 108, 222, 72, (790, 206), ["お任せください。", "終わったら報告します"], 17)
    return (whiteboard + colleagues + hero
            + ebubble(450, 50, 168, 36, (462, 104), ["この企画、こう進めましょう！"], 20)
            + right_bg + sep + label + desk(350, BW, color="#c99a6b").replace('x="-10"', 'x="641"').replace(f'width="{BW + 20}"', 'width="580"')
            + lap + cardsvg + ai_say)


def page2():
    head_band = ('<rect x="200" y="28" width="880" height="96" rx="14" fill="#222"/>'
                 + t(640, 92, "こんな風に、なっていませんか？", 46, fill="#fff", weight="900"))
    msg = (t(640, 618, "理想は、AIにかかりきりになるのではなく", 30, weight="700")
           + '<rect x="596" y="664" width="298" height="20" fill="#ffe57a"/>'
           + t(640, 680, "任せて、あなたが違う価値を生むこと。", 42, weight="900")
           .replace("違う価値を生む", f'<tspan fill="{ACCENT}">違う価値を生む</tspan>'))
    return svg(1280, 720, [(BW, BH)], head_band + panel(40, 148, BW, BH, big_panel()) + msg)


os.makedirs(OUT, exist_ok=True)
for name, fn in (("manga-01.svg", page1), ("manga-02.svg", page2)):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(fn())
print("ok")
