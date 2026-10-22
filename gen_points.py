"""Generate one manga page per key point of the deck (manga-03..06)."""
import os
import sys

from gen import (ACCENT, AI_FILL, AI_STROKE, HAIR, INK, SKIN, arm, desk, drop, ebubble, laptop_back,
                 ml, person, rbubble, sfx, svg, t)

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
W, H = 400, 440
XS = (24, 440, 856)
Y0 = 124


def tw(s, size):
    return sum(size * (0.56 if ord(c) < 128 else 1.0) for c in s)


def tag(label, color):
    w = tw(label, 16) + 28
    return (f'<rect x="12" y="12" width="{w:.0f}" height="32" rx="16" fill="{color}"/>'
            + t(12 + w / 2, 34, label, 16, fill="#fff"))


def before():
    return tag("これまで", "#8a8a8a")


def after(label="こうする"):
    return tag(label, ACCENT)


def panel(x, body, bg="#fff"):
    return (f'<g transform="translate({x},{Y0})"><g clip-path="url(#clip{W}x{H})">'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>{body}</g>'
            f'<rect width="{W}" height="{H}" fill="none" stroke="{INK}" stroke-width="5"/></g>')


def robot(x, y, s=1.0, label=None, cap=False, sleepy=False):
    eyes = ('<path d="M-13,-2 L-5,-2 M5,-2 L13,-2" stroke="#222" stroke-width="3" stroke-linecap="round"/>' if sleepy else
            '<circle cx="-9" cy="-3" r="4.5" fill="#222"/><circle cx="9" cy="-3" r="4.5" fill="#222"/>')
    hat = ('<path d="M-26,-18 Q0,-40 26,-18 Z" fill="#26407a" stroke="#222" stroke-width="2.5"/>'
           '<rect x="-30" y="-20" width="60" height="7" rx="3" fill="#1b2d57"/>'
           '<circle cx="0" cy="-28" r="4" fill="#f5c542"/>' if cap else
           '<path d="M0,-20 L0,-32" stroke="#222" stroke-width="3"/><circle cx="0" cy="-35" r="5" fill="#ffcf4a" stroke="#222" stroke-width="2.5"/>')
    lab = ""
    if label:
        lw = tw(label, 14) + 20
        lab = (f'<rect x="{-lw / 2:.0f}" y="66" width="{lw:.0f}" height="26" rx="13" fill="{AI_STROKE}"/>'
               + t(0, 84, label, 14, fill="#fff"))
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<path d="M-18,34 L-34,48 M18,34 L34,48" stroke="#222" stroke-width="5" stroke-linecap="round"/>'
            f'<rect x="-20" y="22" width="40" height="36" rx="8" fill="{AI_FILL}" stroke="{AI_STROKE}" stroke-width="3"/>'
            + t(0, 46, "AI", 13, fill=AI_STROKE, weight="800")
            + f'<rect x="-26" y="-20" width="52" height="42" rx="12" fill="#fff" stroke="{AI_STROKE}" stroke-width="3"/>'
            + hat + eyes
            + '<path d="M-7,8 Q0,14 7,8" fill="none" stroke="#222" stroke-width="2.5" stroke-linecap="round"/>'
            + lab + '</g>')


def stack(x, top, w, bottom, label, rot):
    lines = "".join(f'<line x1="{x + 4}" y1="{y}" x2="{x + w - 4}" y2="{y}" stroke="#bbb" stroke-width="1.5"/>'
                    for y in range(top + 10, bottom, 9))
    return (f'<rect x="{x}" y="{top}" width="{w}" height="{bottom - top}" fill="#fff" stroke="{INK}" stroke-width="3"/>{lines}'
            f'<g transform="rotate({rot} {x + w / 2} {top})">'
            f'<rect x="{x + w / 2 - tw(label, 15) / 2 - 10:.0f}" y="{top - 16}" width="{tw(label, 15) + 20:.0f}" height="30" '
            f'fill="#ffe57a" stroke="{INK}" stroke-width="2.5"/>' + t(x + w / 2, top + 5, label, 15) + '</g>')


def card(x, y, w, h, title, rows, size=15, accent=AI_STROKE):
    out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#fff" stroke="{INK}" stroke-width="3"/>'
           f'<path d="M{x},{y + 12} a12,12 0 0 1 12,-12 h{w - 24} a12,12 0 0 1 12,12 v26 h-{w} Z" fill="{accent}"/>'
           + t(x + w / 2, y + 26, title, 16, fill="#fff"))
    for i, (r, col) in enumerate(rows):
        out += t(x + 14, y + 64 + i * (size + 13), r, size, anchor="start", fill=col)
    return out


def hourglass(x, y):
    return (f'<g transform="translate({x},{y})">'
            '<path d="M-14,-22 L14,-22 L2,0 L14,22 L-14,22 L-2,0 Z" fill="#fff" stroke="#222" stroke-width="3" stroke-linejoin="round"/>'
            '<path d="M-6,16 L6,16 L0,6 Z M-8,-16 L8,-16 L0,-6 Z" fill="#f2c14e"/>'
            '<path d="M-18,-24 L18,-24 M-18,24 L18,24" stroke="#222" stroke-width="4" stroke-linecap="round"/></g>')


def header(n, title):
    return ('<rect x="24" y="20" width="1232" height="84" rx="14" fill="#222"/>'
            f'<circle cx="74" cy="62" r="26" fill="{ACCENT}"/>' + t(74, 72, str(n), 28, fill="#fff", weight="900")
            + t(118, 75, title, 34, anchor="start", fill="#fff", weight="900"))


def message(pre, hi, post, size=32):
    total = tw(pre + hi + post, size)
    x0 = 640 - total / 2 + tw(pre, size)
    return (f'<rect x="{x0 - 4:.0f}" y="{668 - size * 0.3:.0f}" width="{tw(hi, size) + 8:.0f}" height="{size * 0.42:.0f}" fill="#ffe57a"/>'
            + t(640, 668, f'{pre}<tspan fill="{ACCENT}">{hi}</tspan>{post}', size, weight="900"))


def page(n, title, panels, msg):
    body = header(n, title) + "".join(panel(x, *p) if isinstance(p, tuple) else panel(x, p) for x, p in zip(XS, panels))
    return svg(1280, 720, [(W, H)], body + msg)


def hand(x, y):
    return f'<circle cx="{x}" cy="{y}" r="15" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>'


def screen(x, y, w, h, body):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#3a4152" stroke="#222" stroke-width="3"/>'
            f'<rect x="{x + 9}" y="{y + 9}" width="{w - 18}" height="{h - 18}" rx="4" fill="#1b2130"/>{body}'
            f'<path d="M{x - 20},{y + h} L{x + w + 20},{y + h} L{x + w + 34},{y + h + 16} L{x - 34},{y + h + 16} Z" '
            'fill="#b8c0cc" stroke="#222" stroke-width="3" stroke-linejoin="round"/>')


# ---------- ① Workflow ----------

def page_workflow():
    p1 = (desk(372, W)
          + person(200, 238, "panic", length=150)
          + stack(16, 196, 92, 372, "セキュリティ", -6)
          + stack(292, 170, 92, 372, "仕様書", 5)
          + stack(150, 300, 100, 372, "PR", -3)
          + ebubble(212, 100, 140, 46, (200, 170), ["1つずつ見てたら", "日が暮れる…"], 21)
          + before())
    btn = (screen(40, 236, 196, 128,
                  t(138, 272, "Workflow", 17, fill="#e6edf7")
                  + '<rect x="82" y="290" width="112" height="44" rx="10" fill="#e8483b" stroke="#fff" stroke-width="2"/>'
                  + t(138, 319, "▶ 実行", 19, fill="#fff"))
           + arm("M-40,470 Q60,420 112,334", (118, 326)))
    arrows = "".join(f'<path d="M226,{280 + i * 10} Q262,{y + 40} 282,{y + 20}" fill="none" stroke="{AI_STROKE}" '
                     'stroke-width="3" stroke-dasharray="7 6"/>' for i, y in enumerate((70, 190, 310)))
    p2 = (btn + arrows
          + robot(320, 84, 0.85, "セキュリティ検査")
          + robot(320, 204, 0.85, "抜け漏れチェック")
          + robot(320, 324, 0.85, "PRレビュー")
          + sfx(150, 218, "ポチッ", 30, rot=-10)
          + t(126, 120, "3つのチェックを", 21) + t(126, 150, "並列で一斉スタート", 21)
          + after("Workflow"))
    mug = ('<path d="M196,330 L196,368 Q196,378 206,378 L228,378 Q238,378 238,368 L238,330 Z" fill="#fff" stroke="#222" stroke-width="3"/>'
           '<path d="M238,340 q14,0 14,12 q0,12 -14,12" fill="none" stroke="#222" stroke-width="3"/>'
           '<path d="M208,318 q-6,-10 0,-20 M222,318 q-6,-10 0,-20" fill="none" stroke="#aaa" stroke-width="2.5" stroke-linecap="round"/>')
    p3 = (desk(380, W)
          + person(110, 262, "happy", length=150)
          + mug + hand(186, 360)
          + card(196, 56, 190, 214, "検査レポート",
                 [("✓ セキュリティ 指摘1", INK), ("✓ 抜け漏れ 指摘2", INK), ("✓ PRレビュー 指摘3", INK),
                  ("検証済みの指摘だけ", "#2fa36b")], size=14)
          + ebubble(104, 128, 88, 44, (110, 196), ["指摘だけ", "見ればOK！"], 19)
          + after("結果"))
    return page(1, "Workflowでチェック系をまとめて任せる", [p1, p2, p3],
                message("セキュリティ検査・抜け漏れ・PRレビューは", "丸ごと任せる", ""))


# ---------- ② /loop ----------

def page_loop():
    note = (card(18, 58, 210, 168, "毎朝のルーティン",
                 [("□ 新着PRチェック", INK), ("□ CIの失敗確認", INK), ("□ Issue整理", INK), ("□ 依頼メール確認", INK)], size=15,
                 accent="#8a8a8a"))
    clock = ('<g transform="translate(330,92)"><circle r="34" fill="#fff" stroke="#222" stroke-width="3"/>'
             '<path d="M0,0 L0,-22 M0,0 L-16,0" stroke="#222" stroke-width="3.5" stroke-linecap="round"/></g>'
             + t(330, 150, "9:00", 18))
    bored = person(280, 270, "intense", length=140)
    p1 = (desk(380, W) + bored + note + clock
          + ebubble(104, 300, 84, 42, (230, 285), ["毎朝これで", "1時間…"], 18)
          + before())
    term = ('<rect x="18" y="56" width="364" height="86" rx="10" fill="#1b2130" stroke="#222" stroke-width="3"/>'
            + t(34, 90, "&gt; /loop 30m", 19, anchor="start", fill="#9ef0b8")
            + t(34, 122, "  新着PRとCIを巡回して報告", 19, anchor="start", fill="#e6edf7"))
    path = ('<ellipse cx="285" cy="372" rx="96" ry="34" fill="none" stroke="#26407a" stroke-width="3" stroke-dasharray="10 8"/>'
            '<path d="M372,360 l10,14 l-16,4" fill="none" stroke="#26407a" stroke-width="3" stroke-linejoin="round"/>')
    light = '<path d="M326,300 L392,272 L392,336 Z" fill="#fff3a6" opacity="0.8"/>'
    p2 = (person(96, 266, "determined", length=150)
          + laptop_back(96, 330, w=150, h=80)
          + path + light
          + robot(290, 296, 1.0, "30分ごとに巡回", cap=True)
          + sfx(290, 210, "巡回開始！", 28, rot=-6)
          + term + after("/loop"))
    colleague = ('<g transform="translate(336,396)"><path d="M-66,110 Q-66,34 0,34 Q66,34 66,110 Z" fill="#6c8f5a" stroke="#222" stroke-width="3"/>'
                 f'<circle r="38" fill="{HAIR}" stroke="#222" stroke-width="3"/></g>')
    p3 = (person(110, 330, "happy", length=200)
          + colleague
          + card(150, 52, 238, 178, "● 巡回レポート",
                 [("新着PR 2件：レビュー済", INK), ("CI失敗 1件：原因メモ有", INK), ("あなたの判断待ち：1件", ACCENT)], size=15)
          + ebubble(96, 236, 90, 40, (110, 284), ["気になるのだけ", "見ればOK"], 17)
          + after("結果"))
    return page(2, "/loop で巡回させて、日課を自動化する", [p1, p2, p3],
                message("毎朝のチェックはAIが巡回。あなたは", "報告だけ拾う", ""))


# ---------- ③ answer the easy ones first ----------

def page_parallel():
    qs = rbubble(132, 52, 256, 116, (120, 110),
                 ["Q1 全体の設計方針は？", "Q2 テストも追加する？", "Q3 この命名でOK？"], 16, anchor="start")
    p1 = (robot(66, 104, 1.1, sleepy=True) + qs
          + t(106, 74, "z", 18, fill="#888") + t(122, 60, "Z", 22, fill="#888")
          + hourglass(320, 230) + t(320, 286, "AI待機中…", 15, fill="#555")
          + person(110, 300, "panic", length=150)
          + ebubble(290, 360, 100, 44, (170, 330), ["Q1が決まらず", "全部止まる…"], 18)
          + before())
    run = ""
    for y, lab in ((150, "Q2 実行中"), (300, "Q3 実行中")):
        run += (f'<path d="M232,{y + 10} L260,{y + 10} M224,{y + 26} L256,{y + 26} M236,{y + 42} L262,{y + 42}" '
                f'stroke="{AI_STROKE}" stroke-width="3" stroke-linecap="round"/>' + robot(310, y, 0.95, lab))
    p2 = (person(108, 250, "determined", length=170)
          + run
          + ebubble(206, 86, 172, 50, (130, 182), ["Q2はYes、Q3はOK！", "先に進めといて"], 19)
          + sfx(46, 190, "即答", 26, rot=-12)
          + after())
    bars = (card(204, 120, 186, 128, "バックグラウンド", [], accent=AI_STROKE)
            + t(218, 186, "Q2", 15, anchor="start") + '<rect x="250" y="172" width="126" height="16" rx="8" fill="#e3e8f0"/>'
            '<rect x="250" y="172" width="92" height="16" rx="8" fill="#3b6fd8"/>'
            + t(218, 224, "Q3", 15, anchor="start") + '<rect x="250" y="210" width="126" height="16" rx="8" fill="#2fa36b"/>'
            + t(313, 223, "完了", 12, fill="#fff"))
    chart = (t(200, 352, "AIが止まっている時間", 16)
             + t(16, 384, "これまで", 14, anchor="start") + '<rect x="90" y="370" width="290" height="20" rx="4" fill="#d9534f"/>'
             + t(16, 420, "こうする", 14, anchor="start") + '<rect x="90" y="406" width="64" height="20" rx="4" fill="#2fa36b"/>')
    p3 = (person(100, 212, "happy", length=110)
          + ebubble(104, 82, 92, 40, (104, 150), ["Q1はじっくり", "考えよう"], 17)
          + bars + '<line x1="16" y1="330" x2="384" y2="330" stroke="#ccc" stroke-width="2"/>' + chart
          + after("その間に"))
    return page(3, "すぐ答えられる問いから返して、裏で進めさせる", [p1, p2, p3],
                message("答えやすい問いから返して、", "AIを止めない", ""))


# ---------- ④ prepare so questions are closed ----------

def page_closed():
    paper = ('<rect x="236" y="176" width="148" height="290" fill="#fff" stroke="#222" stroke-width="3"/>'
             + t(310, 204, "回答（長文）", 15)
             + "".join(f'<line x1="250" y1="{y}" x2="{370 - (y * 7) % 40}" y2="{y}" stroke="#bbb" stroke-width="3"/>'
                       for y in range(222, 440, 16)))
    p1 = (robot(64, 92, 0.95)
          + rbubble(126, 52, 260, 78, (104, 92), ["今後の方針は", "どうしますか？"], 19)
          + person(124, 290, "panic", length=150)
          + laptop_back(124, 354, w=150, h=70)
          + paper
          + sfx(110, 196, "うーん…", 24, rot=0, fill="#555")
          + before())
    clip = ('<rect x="138" y="58" width="246" height="300" rx="10" fill="#c99a6b" stroke="#222" stroke-width="3"/>'
            '<rect x="152" y="80" width="218" height="266" fill="#fff" stroke="#222" stroke-width="2"/>'
            '<rect x="226" y="48" width="70" height="22" rx="6" fill="#888" stroke="#222" stroke-width="2.5"/>'
            + t(261, 114, "段取り表", 22)
            + "".join(t(170, 156 + i * 40, f'<tspan fill="#2fa36b">✓</tspan> {s}', 19, anchor="start")
                      for i, s in enumerate(["ゴール", "制約・前提", "判断の基準", "完了の条件", "選択肢と推奨"])))
    p2 = (clip
          + person(74, 360, "determined", length=120)
          + ebubble(70, 232, 60, 44, (74, 300), ["先に", "渡す！"], 18)
          + after())
    p3 = (robot(64, 92, 0.95)
          + rbubble(126, 46, 260, 92, (104, 92), ["A案とB案どちらに？", "（推奨：A案）"], 19)
          + person(120, 300, "happy", length=110)
          + ebubble(282, 268, 64, 40, (176, 286), ["A！"], 28)
          + sfx(300, 196, "一言で", 28, rot=-8)
          + t(200, 428, "→ AIはそのまま続行", 18, fill=AI_STROKE)
          + after())
    return page(4, "段取りを固めて、オープンクエスチョンをさせない", [p1, p2, p3],
                message("段取りを先に渡せば、AIへの返事は", "一言で済む", ""))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (("manga-03.svg", page_workflow), ("manga-04.svg", page_loop),
                     ("manga-05.svg", page_parallel), ("manga-06.svg", page_closed)):
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(fn())
    print("ok")
