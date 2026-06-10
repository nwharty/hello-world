#!/usr/bin/env python3
"""Renders the 10-image Etsy listing carousel (1080x1350) with PIL.

Faithful recreation of the design handoff (listing-cards-1/2.jsx + brand.css)
using the real brand fonts (Spectral / Hanken Grotesk / Spline Sans Mono).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
OUT = "/home/user/hello-world/executor-kit/listing"
FD = "/tmp/fonts"

# ---- tokens ----
NAVY = (34, 58, 82)
NAVY_G1 = (39, 66, 93)
NAVY_G2 = (23, 40, 56)
PAPER = (250, 247, 241)
PAPER2 = (244, 237, 225)
WHITE = (255, 253, 249)
ZEBRA = (249, 244, 235)
SAGE = (231, 239, 229)
SAGE_DEEP = (196, 214, 192)
SAGE_INK = (74, 100, 80)
GOLD = (181, 138, 52)
GOLD_SOFT = (212, 177, 100)
GOLD_PALE = (236, 220, 180)
GOLD_TEXT = (124, 93, 26)
CLAY = (189, 123, 92)
OK = (93, 138, 99)
CHIP_TODO = (238, 241, 244)


def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def alpha_on(fg, bg, a):
    return mix(bg, fg, a)


INK70 = alpha_on(NAVY, PAPER, 0.70)
INK55 = alpha_on(NAVY, PAPER, 0.55)
INK40 = alpha_on(NAVY, PAPER, 0.40)
LINE = alpha_on(NAVY, WHITE, 0.13)
LINE_SOFT = alpha_on(NAVY, WHITE, 0.08)


def ink(bg, a):
    return alpha_on(NAVY, bg, a)


_fc = {}


def F(kind, size):
    key = (kind, size)
    if key not in _fc:
        files = {"serif": "Spectral-500.ttf", "serif6": "Spectral-600.ttf", "sans": "Hanken-400.ttf",
                 "sans6": "Hanken-600.ttf", "sans7": "Hanken-700.ttf", "mono": "SplineMono-500.ttf"}
        _fc[key] = ImageFont.truetype(os.path.join(FD, files[kind]), size)
    return _fc[key]


def tw(d, text, font):
    return d.textlength(text, font=font)


def tracked(d, xy, text, font, fill, tracking):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking
    return x - tracking


def eyebrow(d, xy, text, size=13, color=GOLD):
    f = F("mono", size)
    tracked(d, xy, text.upper(), f, color, size * 0.22)


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def para(d, xy, text, font, fill, maxw, lh):
    x, y = xy
    for ln in wrap(d, text, font, maxw):
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def rr(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def star4(d, cx, cy, s, fill):
    pts = [(0, -s), (0.2 * s, -0.2 * s), (s, 0), (0.2 * s, 0.2 * s), (0, s), (-0.2 * s, 0.2 * s), (-s, 0), (-0.2 * s, -0.2 * s)]
    d.polygon([(cx + x, cy + y) for x, y in pts], fill=fill)


def mark(d, cx, cy, dia):
    r = dia / 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY)
    d.ellipse([cx - r + 2, cy - r + 2, cx + r - 2, cy + r - 2], outline=alpha_on(GOLD_SOFT, NAVY, 0.5), width=2)
    star4(d, cx, cy, r * 0.42, GOLD_SOFT)


def wordmark(d, x, y, size=19, color=NAVY):
    dia = size * 1.5
    mark(d, x + dia / 2, y + dia / 2, dia)
    f = F("serif", size)
    d.text((x + dia + size * 0.6, y + dia / 2 - size * 0.62), "The Executor Kit", font=f, fill=color)


def star5(d, cx, cy, s, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = s if i % 2 == 0 else s * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill)


def stars(d, x, y, s=11, gap=7):
    for i in range(5):
        star5(d, x + i * (2 * s + gap) + s, y + s, s, GOLD)
    return x + 5 * (2 * s + gap)


def chip(d, x, y, text, kind, size=15):
    f = F("sans6", size)
    pad = size * 0.75
    h = size * 1.9
    wdt = tw(d, text, f) + 2 * pad + (size if kind == "done" else 0)
    colors = {"done": (SAGE, SAGE_INK), "prog": (GOLD_PALE, GOLD_TEXT), "todo": (CHIP_TODO, INK55)}
    bg, fg = colors[kind]
    rr(d, [x, y, x + wdt, y + h], h / 2, fill=bg)
    tx = x + pad
    if kind == "done":
        cx, cy = x + pad + 3, y + h / 2
        d.line([(cx - 4, cy), (cx - 1, cy + 4), (cx + 6, cy - 4)], fill=fg, width=3, joint="curve")
        tx += size
    d.text((tx, y + h / 2 - size * 0.62), text, font=f, fill=fg)
    return wdt, h


CHIP_LABEL = {"done": "Done", "prog": "In progress", "todo": "Not started"}

TABS = [("Start Here", GOLD), ("First 30 Days", NAVY), ("Task Log", None), ("Key Contacts", None),
        ("Documents", None), ("Notifications", None), ("Assets", GOLD), ("Debts", None), ("Services", None),
        ("Estate Ledger", GOLD), ("Distributions", None), ("Final Accounting", (176, 0, 32))]


def tab_strip(d, x0, y0, wdt, active):
    h = 42
    d.rectangle([x0, y0, x0 + wdt, y0 + h], fill=PAPER)
    d.line([(x0, y0), (x0 + wdt, y0)], fill=LINE, width=1)
    f = F("sans6", 12)
    fb = F("sans7", 12)
    x = x0 + 12
    for name, color in TABS:
        is_a = name == active
        fnt = fb if is_a else f
        cw = tw(d, name, fnt) + 28 + 15
        if x + cw > x0 + wdt - 8:
            break
        if is_a:
            rr(d, [x, y0 + 12, x + cw, y0 + h], 8, fill=WHITE)
            d.rectangle([x, y0 + h - 3, x + cw, y0 + h], fill=GOLD)
        sw = color if color else LINE
        d.rectangle([x + 14, y0 + 23, x + 22, y0 + 31], fill=sw)
        d.text((x + 29, y0 + 19), name, font=fnt, fill=NAVY if is_a else INK55)
        x += cw + 2


def sheet_frame(width, rows, cols, active="First 30 Days", title=None, subtitle=None, name="Executor_Estate_Kit.xlsx",
                row_h=56, header_h=46):
    """rows: list of lists of cell dicts {t, kind} kind in strong/muted/phase/money/chip:done..."""
    th = 46 + (96 if title else 0) + header_h + len(rows) * row_h + 42
    img = Image.new("RGB", (width, th), WHITE)
    d = ImageDraw.Draw(img)
    # toolbar
    d.rectangle([0, 0, width, 46], fill=PAPER)
    d.line([(0, 46), (width, 46)], fill=LINE, width=1)
    for i, c in enumerate([(230, 163, 154), (232, 207, 143), (169, 205, 170)]):
        d.ellipse([18 + i * 25, 17, 29 + i * 25, 28], fill=c)
    d.text((96, 14), name, font=F("sans6", 15), fill=NAVY)
    tag = "EXCEL · GOOGLE SHEETS"
    d.text((width - tw(d, tag, F("mono", 11)) - 18 - 11 * 0.08 * len(tag), 16), tag, font=F("mono", 11), fill=INK55)
    y = 46
    if title:
        d.text((26, y + 18), title, font=F("serif", 30), fill=NAVY)
        if subtitle:
            d.text((26, y + 60), subtitle, font=F("sans", 15), fill=INK55)
        y += 96
        d.line([(0, y), (width, y)], fill=LINE_SOFT, width=1)
    # header
    d.rectangle([0, y, width, y + header_h], fill=NAVY)
    x = 0
    fh = F("sans6", 12)
    for label, cw in cols:
        d.text((x + 16, y + header_h / 2 - 8), label, font=fh, fill=PAPER)
        x += cw
    y += header_h
    for ri, row in enumerate(rows):
        if ri % 2 == 1:
            d.rectangle([0, y, width, y + row_h], fill=alpha_on(PAPER2, WHITE, 0.45))
        x = 0
        for ci, cell in enumerate(row):
            cwd = cols[ci][1]
            t, kind = cell.get("t", ""), cell.get("kind", "muted")
            cy = y + row_h / 2
            if kind == "phase":
                tracked(d, (x + 16, cy - 7), t.upper(), F("mono", 11), GOLD, 0.7)
            elif kind == "strong":
                lines = wrap(d, t, F("sans6", 14), cwd - 30)[:2]
                yy = cy - 9 * len(lines)
                for ln in lines:
                    d.text((x + 16, yy), ln, font=F("sans6", 14), fill=NAVY)
                    yy += 19
            elif kind == "money":
                d.text((x + 16, cy - 9), t, font=F("sans7", 14), fill=cell.get("color", NAVY))
            elif kind.startswith("chip:"):
                k = kind.split(":")[1]
                chip(d, x + 14, cy - 14, CHIP_LABEL[k], k, 12)
            else:
                lines = wrap(d, t, F("sans", 13), cwd - 30)[:2]
                yy = cy - 8 * len(lines)
                for ln in lines:
                    d.text((x + 16, yy), ln, font=F("sans", 13), fill=INK55)
                    yy += 17
            x += cwd
        y += row_h
        d.line([(0, y), (width, y)], fill=LINE_SOFT, width=1)
    tab_strip(d, 0, th - 42, width, active)
    return img


def round_mask_paste(base, img, xy, radius, shadow=True):
    if shadow:
        sh = Image.new("RGBA", (img.width + 80, img.height + 80), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sh)
        sd.rounded_rectangle([40, 48, 40 + img.width, 48 + img.height], radius=radius, fill=(24, 43, 62, 60))
        from PIL import ImageFilter
        sh = sh.filter(ImageFilter.GaussianBlur(22))
        base.paste(Image.alpha_composite(base.crop((xy[0] - 40, xy[1] - 40, xy[0] + img.width + 40, xy[1] + img.height + 40)).convert("RGBA"), sh).convert("RGB"), (xy[0] - 40, xy[1] - 40))
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width, img.height], radius=radius, fill=255)
    base.paste(img, xy, m)


def gradient(wd, ht, c1, c2, angle_diag=True):
    img = Image.new("RGB", (wd, ht))
    px = img.load()
    for yy in range(ht):
        for xx in range(0, wd, 4):
            t = ((xx / wd) * 0.35 + (yy / ht) * 0.65) if angle_diag else yy / ht
            c = mix(c1, c2, t)
            for k in range(4):
                if xx + k < wd:
                    px[xx + k, yy] = c
    return img


def guide_cover(wdt, label=True):
    ht = int(wdt * 1.29)
    img = gradient(wdt, ht, NAVY_G1, (26, 46, 66))
    d = ImageDraw.Draw(img)
    inset = 9
    rr(d, [inset, inset, wdt - inset, ht - inset], 12, outline=alpha_on(GOLD_SOFT, NAVY_G2, 0.35), width=1)
    rr(d, [inset + 3, inset + 3, wdt - inset - 3, ht - inset - 3], 10, outline=alpha_on(GOLD_SOFT, NAVY_G2, 0.12), width=5)
    pad = int(wdt * 0.12)
    mk = int(wdt * 0.2)
    mark(d, pad + mk / 2, pad + mk / 2, mk)
    y = ht - pad - int(wdt * 0.135 * 2.6) - (int(wdt * 0.05 * 2.8) if True else 0) - int(wdt * 0.1)
    if label:
        eyebrow(d, (pad, y), "The companion guide", max(int(wdt * 0.044), 8), GOLD_SOFT)
        y += int(wdt * 0.044) + 12
    tsize = int(wdt * 0.135)
    while tw(d, "The Executor's", F("serif", tsize)) > wdt - 2 * pad and tsize > 8:
        tsize -= 1
    f = F("serif", tsize)
    d.text((pad, y), "The Executor's", font=f, fill=PAPER)
    d.text((pad, y + int(wdt * 0.135 * 1.06)), "First 30 Days", font=f, fill=PAPER)
    y += int(wdt * 0.135 * 2.12) + 16
    d.rectangle([pad, y, pad + int(wdt * 0.22), y + 3], fill=GOLD)
    y += 17
    fs = F("sans", int(wdt * 0.05))
    for ln in wrap(d, "A calm, step-by-step walkthrough of the critical first month.", fs, wdt - 2 * pad):
        d.text((pad, y), ln, font=fs, fill=alpha_on(PAPER, NAVY_G2, 0.7))
        y += int(wdt * 0.05 * 1.4)
    return img


def card_top(d, i, dark=False):
    wordmark(d, 70, 64, 19, PAPER if dark else NAVY)
    f = F("mono", 14)
    t = f"{i:02d} / 10"
    tracked(d, (W - 70 - tw(d, t, f) - len(t) * 14 * 0.16, 70), t, f, alpha_on(PAPER, NAVY, 0.55) if dark else INK40, 14 * 0.16)


def shell(bg):
    img = Image.new("RGB", (W, H), bg)
    return img, ImageDraw.Draw(img)


def headline(d, y, eb, lines, size, color=NAVY, eb_color=GOLD, x=70):
    eyebrow(d, (x, y), eb, 13, eb_color)
    y += 34
    f = F("serif", size)
    for ln in lines:
        d.text((x - 3, y), ln, font=f, fill=color)
        y += int(size * 1.06)
    return y


# ============================================================ cards
def card01():
    img, d = shell(PAPER)
    card_top(d, 1)
    y = headline(d, 132, "Instant digital download", ["The complete", "executor system."], 74)
    f = F("sans", 25)
    y = para(d, (70, y + 16), "A 12-tab workbook and a 30-day guide that give every task, document, dollar, and deadline a place to live — so nothing rests on your memory during the hardest month to rely on it.", f, INK70, 720, 36)
    cols = [("Priority", 110), ("Task", 420), ("Status", 166)]
    rows = [
        [{"t": "Week 1", "kind": "phase"}, {"t": "Locate the original will & codicils", "kind": "strong"}, {"kind": "chip:done"}],
        [{"t": "Week 1", "kind": "phase"}, {"t": "Order 10–15 certified death certificates", "kind": "strong"}, {"kind": "chip:done"}],
        [{"t": "Week 2", "kind": "phase"}, {"t": "File petition for probate with the court", "kind": "strong"}, {"kind": "chip:prog"}],
        [{"t": "Week 2", "kind": "phase"}, {"t": "Open an estate checking account", "kind": "strong"}, {"kind": "chip:todo"}],
        [{"t": "Week 3–4", "kind": "phase"}, {"t": "Begin asset inventory at date-of-death value", "kind": "strong"}, {"kind": "chip:todo"}],
    ]
    sheet = sheet_frame(696, rows, cols, title="The First 30 Days", subtitle="Work top to bottom. Done and N/A both count as finished.", row_h=52)
    sheet = sheet.rotate(1.2, expand=True, fillcolor=PAPER, resample=Image.BICUBIC)
    img.paste(sheet, (58, y + 26))
    gc = guide_cover(272)
    round_mask_paste(img, gc, (W - 70 - 272 + 8, H - 156 - gc.height + 16), 14)
    yb = H - 130
    d.line([(70, yb), (W - 70, yb)], fill=LINE, width=1)
    x = stars(d, 70, yb + 26)
    f = F("sans6", 19)
    d.text((x + 18, yb + 22), "Excel + Google Sheets", font=f, fill=INK70)
    x2 = x + 18 + tw(d, "Excel + Google Sheets", f) + 18
    d.ellipse([x2, yb + 33, x2 + 5, yb + 38], fill=INK40)
    d.text((x2 + 18, yb + 22), "12-tab workbook + 30-day guide", font=f, fill=INK70)
    return img


def card02():
    img, d = shell(PAPER)
    card_top(d, 2)
    y = headline(d, 134, "What's inside", ["Twelve tabs, in the order", "the job actually happens."], 56)
    tabs = [("01", "First 30 Days", "What's urgent, what can wait"), ("02", "Task Log", "Every call & letter, documented"),
            ("03", "Key Contacts", "Everyone you'll call twice"), ("04", "Documents", "Where every paper lives"),
            ("05", "Notifications", "Who to tell + cert. copies"), ("06", "Assets", "Full date-of-death inventory"),
            ("07", "Debts", "Verified before a dollar is paid"), ("08", "Services", "Subscriptions to cancel"),
            ("09", "Estate Ledger", "Every dollar in and out"), ("10", "Distributions", "Who received what, signed"),
            ("11", "Final Accounting", "The court summary, automatic"), ("12", "Start Here", "Read-me + Google Sheets setup")]
    y += 30
    cw, ch, gap = (W - 140 - 16) // 2, 132, 16
    for i, (n, name, desc) in enumerate(tabs):
        cx = 70 + (i % 2) * (cw + gap)
        cy = y + (i // 2) * (ch + gap)
        rr(d, [cx, cy, cx + cw, cy + ch], 14, fill=WHITE)
        d.text((cx + 22, cy + ch / 2 - 22), n, font=F("serif", 30), fill=GOLD)
        d.text((cx + 80, cy + 30), name, font=F("sans7", 21), fill=NAVY)
        d.text((cx + 80, cy + 64), desc, font=F("sans", 15), fill=INK55)
    return img


def card03():
    img, d = shell(SAGE)
    card_top(d, 3)
    y = headline(d, 130, "Tab 01 · First 30 Days", ["Know what's urgent —", "and what can wait."], 56)
    y = para(d, (70, y + 14), "Estate settlement is a sequence, not a pile. The checklist is ordered by priority, so you always know the one next right thing.", F("sans", 23), ink(SAGE, 0.70), 760, 33)
    rows_src = [
        ("Week 1", "Locate the original will (and any codicils)", "Check the safe, desk, attorney, bank box.", "done"),
        ("Week 1", "Order 10–15 certified death certificates", "Every institution wants its own copy.", "done"),
        ("Week 1", "Secure the home, vehicles & valuables", "You protect estate property from now on.", "done"),
        ("Week 2", "File the will & petition for probate", "Nothing official happens until you're appointed.", "prog"),
        ("Week 2", "Get an EIN, then open an estate account", "The estate is its own taxpayer.", "prog"),
        ("Week 2–3", "Notify SSA, employer, insurers & banks", "Benefits stop; accounts freeze or retitle.", "todo"),
        ("Week 3–4", "Begin the asset inventory", "Date-of-death values become your opening balance.", "todo"),
    ]
    cols = [("Priority", 116), ("Task", 330), ("Why it matters", 334), ("Status", 160)]
    rows = [[{"t": p_, "kind": "phase"}, {"t": t, "kind": "strong"}, {"t": w_, "kind": "muted"}, {"kind": "chip:" + s}] for p_, t, w_, s in rows_src]
    sheet = sheet_frame(W - 140, rows, cols, row_h=86)
    round_mask_paste(img, sheet, (70, y + 40), 14)
    return img


def card04():
    img, d = shell(NAVY)
    card_top(d, 4, dark=True)
    y = headline(d, 130, "The part that actually trips people up", ["The hardest report", "writes itself."], 60, PAPER, GOLD_SOFT)
    para(d, (70, y + 14), "Courts and beneficiaries are entitled to a formal accounting of every dollar. Fill in the tabs as you go and the Final Accounting builds itself — in the exact structure they expect.", F("sans", 23), alpha_on(PAPER, NAVY, 0.72), 770, 33)
    lines = [("Beginning inventory", "at date-of-death value", "$842,300.00", False),
             ("+ Receipts during administration", "asset sales, refunds, income", "$ 38,910.00", False),
             ("– Disbursements", "debts, fees, taxes, upkeep", "$ 71,540.00", False),
             ("– Distributions to beneficiaries", "with signed releases", "$ 305,000.00", False),
             ("Remaining estate balance", "matches the estate bank account", "$504,670.00", True)]
    cw = W - 140
    ch = 66 + 4 * 84 + 12 + 118 + 26
    cy0 = H - 90 - ch
    panel = Image.new("RGB", (cw, ch), WHITE)
    pd = ImageDraw.Draw(panel)
    tracked(pd, (34, 28), "FINAL ACCOUNTING SUMMARY", F("mono", 13), alpha_on(NAVY, WHITE, 0.55), 13 * 0.14)
    yy = 66
    for a, b_, v, total in lines:
        if total:
            yy += 12
            rr(pd, [18, yy, cw - 18, yy + 118], 12, fill=SAGE)
            pd.rectangle([18, yy, cw - 18, yy + 3], fill=NAVY)
            pd.text((36, yy + 22), a, font=F("sans7", 24), fill=NAVY)
            pd.text((36, yy + 60), b_, font=F("sans", 14), fill=ink(SAGE, 0.55))
            pd.text((cw - 36 - tw(pd, v, F("sans7", 30)), yy + 34), v, font=F("sans7", 30), fill=NAVY)
        else:
            pd.line([(18, yy), (cw - 18, yy)], fill=LINE_SOFT, width=1)
            pd.text((18, yy + 14), a, font=F("sans6", 20), fill=NAVY)
            pd.text((18, yy + 46), b_, font=F("sans", 14), fill=INK55)
            pd.text((cw - 18 - tw(pd, v, F("sans7", 21)), yy + 22), v, font=F("sans7", 21), fill=INK70)
            yy += 84
    round_mask_paste(img, panel, (70, cy0), 18)
    # clay badge
    bf = F("sans7", 18)
    bt = "calculates itself"
    bw = int(tw(d, bt, bf)) + 64
    badge = Image.new("RGBA", (bw, 46), (0, 0, 0, 0))
    bd = ImageDraw.Draw(badge)
    rr(bd, [0, 0, bw - 1, 45], 23, fill=CLAY)
    bd.text((20, 10), bt, font=bf, fill=(255, 255, 255))
    star4(bd, bw - 26, 23, 8, (255, 255, 255))
    badge = badge.rotate(-3, expand=True, resample=Image.BICUBIC)
    img.paste(badge, (W - 70 - badge.width + 10, cy0 - 26), badge)
    return img


def card05():
    img, d = shell(PAPER2)
    card_top(d, 5)
    y = headline(d, 130, "The companion guide · PDF", ["Start calm. A guide that", "sequences the whole job."], 56)
    gc = guide_cover(380)
    round_mask_paste(img, gc, (70, y + 210), 14)
    x = 70 + 380 + 48
    yy = para(d, (x, y + 230), "Most kits hand you empty tables. This one opens with a calm walkthrough of the critical first month — including:", F("sans", 23), ink(PAPER2, 0.70), 440, 33)
    items = [("The three rules", "that protect you from personal liability"),
             ("Week-by-week sequence", "protect & gather → appointment → notify → inventory"),
             ("The five mistakes", "that cost executors their own money"),
             ("When to get help", "and why the estate — not you — pays for it")]
    yy += 26
    for a, b_ in items:
        d.ellipse([x, yy, x + 30, yy + 30], fill=SAGE)
        d.line([(x + 8, yy + 15), (x + 13, yy + 21), (x + 22, yy + 9)], fill=SAGE_INK, width=3, joint="curve")
        d.text((x + 44, yy), a, font=F("sans7", 20), fill=NAVY)
        yy = para(d, (x + 44, yy + 30), b_, F("sans", 16), ink(PAPER2, 0.55), 420, 22) + 26
    return img


def card06():
    img, d = shell(SAGE)
    card_top(d, 6)
    y = headline(d, 130, "Instant download · nothing ships", ["Everything you get,", "the moment you buy."], 56)
    y += 30
    gap = 16
    cw = (W - 140 - gap) // 2

    def tile(cx, cy, wdt, ht, label, title):
        rr(d, [cx, cy, cx + wdt, cy + ht], 16, fill=WHITE)
        eyebrow(d, (cx + 24, cy + 24), label, 12)
        d.text((cx + 24, cy + 48), title, font=F("serif", 26), fill=NAVY)

    # workbook tile (span 2)
    tile(70, y, W - 140, 296, "The workbook", "12-tab Estate Workbook")
    msx, msy, msw = 94, y + 96, W - 188
    rr(d, [msx, msy, msx + msw, msy + 168], 10, fill=WHITE, outline=LINE_SOFT, width=1)
    d.rectangle([msx, msy, msx + msw, msy + 22], fill=NAVY)
    for i in range(6):
        ry = msy + 22 + i * 24
        if i % 2:
            d.rectangle([msx, ry, msx + msw, ry + 24], fill=alpha_on(PAPER2, WHITE, 0.5))
        d.rectangle([msx + 12, ry + 8, msx + 12 + msw * 0.36, ry + 16], fill=LINE)
        d.rectangle([msx + 24 + msw * 0.36, ry + 8, msx + 24 + msw * 0.78, ry + 16], fill=LINE_SOFT)
        d.rectangle([msx + msw - 46, ry + 8, msx + msw - 12, ry + 16], fill=SAGE_DEEP if i < 2 else GOLD_PALE)
    y2 = y + 296 + gap
    ht2 = 296
    tile(70, y2, cw, ht2, "The guide", "The Executor's First 30 Days")
    gc = guide_cover(140, label=False)
    img.paste(gc, (70 + cw // 2 - 70, y2 + 100))
    tile(70 + cw + gap, y2, cw, ht2, "Both formats — one purchase", "Excel + Google Sheets")
    px = 70 + cw + gap + 24
    py = y2 + 110
    f = F("sans6", 16)
    w1 = tw(d, "Excel .xlsx", f) + 32
    rr(d, [px, py, px + w1, py + 40], 20, fill=NAVY)
    d.text((px + 16, py + 9), "Excel .xlsx", font=f, fill=PAPER)
    rr(d, [px + w1 + 10, py, px + w1 + 10 + tw(d, "Google Sheets", f) + 32, py + 40], 20, outline=LINE, width=2)
    d.text((px + w1 + 26, py + 9), "Google Sheets", font=f, fill=NAVY)
    y3 = y2 + ht2 + gap
    ht3 = 296
    tile(70, y3, cw, ht3, "The differentiator", "Automatic Final Accounting")
    para(d, (94, y3 + 96), "The court-ready summary totals itself as you go.", F("sans", 16), ink(WHITE, 0.55), cw - 48, 23)
    tile(70 + cw + gap, y3, cw, ht3, "Setup", "Works in minutes")
    para(d, (70 + cw + gap + 24, y3 + 96), "Open in Excel, or upload to Google Sheets — free, instructions included.", F("sans", 16), ink(WHITE, 0.55), cw - 48, 23)
    return img


def card07():
    img, d = shell(NAVY)
    card_top(d, 7, dark=True)
    y = headline(d, 132, "What attorneys say actually burns executors", ["Three rules that protect", "you personally."], 60, PAPER, GOLD_SOFT)
    para(d, (70, y + 14), "Almost every costly executor mistake breaks one of these. The guide opens with them — so you're protected from page one.", F("sans", 22), alpha_on(PAPER, NAVY, 0.7), 720, 31)
    rules = [("01", "Never mix estate money with your own", "Commingling funds is the fastest way to become personally liable — even with perfect intentions."),
             ("02", "Distribute nothing until debts & taxes are settled", "If the money later runs short, the difference can come out of your pocket. The law puts creditors first."),
             ("03", "Write everything down", "Every call, letter, and dollar. Beneficiaries are entitled to an accounting you can't rebuild from memory.")]
    ch, gap = 178, 16
    y0 = H - 90 - 3 * ch - 2 * gap
    for i, (n, t, ds) in enumerate(rules):
        cy = y0 + i * (ch + gap)
        rr(d, [70, cy, W - 70, cy + ch], 16, fill=alpha_on(PAPER, NAVY, 0.06), outline=alpha_on(GOLD_SOFT, NAVY, 0.22), width=1)
        d.text((100, cy + 36), n, font=F("serif", 46), fill=GOLD_SOFT)
        d.text((196, cy + 30), t, font=F("serif", 28), fill=PAPER)
        para(d, (196, cy + 76), ds, F("sans", 18), alpha_on(PAPER, NAVY, 0.66), 720, 26)
    return img


def card08():
    img, d = shell(PAPER2)
    card_top(d, 8)
    y = headline(d, 128, "Notifications tab · no competitor tracks this", ["The one thing every", "executor runs out of."], 56)
    y = para(d, (70, y + 14), "You'll need 10–15 certified death certificates, and every institution wants its own. The tracker shows exactly where each copy went — and how many you have left.", F("sans", 22), ink(PAPER2, 0.70), 720, 31)
    rows_src = [("Social Security Admin.", "Yes", "1", "done"), ("Life insurance company", "Yes", "2", "done"),
                ("Banks — each account", "Yes", "4", "done"), ("Brokerage / investments", "Yes", "2", "prog"),
                ("DMV — vehicle titles", "Yes", "1", "prog"), ("Employer / HR", "Unsure", "1", "todo")]
    cols = [("Who to notify", 250), ("Cert. copy?", 116), ("Used", 86), ("Status", 168)]
    rows = [[{"t": a, "kind": "strong"}, {"t": b_, "kind": "muted"}, {"t": c, "kind": "money"}, {"kind": "chip:" + s}] for a, b_, c, s in rows_src]
    sheet = sheet_frame(620, rows, cols, active="Notifications", row_h=78)
    round_mask_paste(img, sheet, (70, y + 56), 14)
    # stat card
    sx, sw = 70 + 620 + 22, W - 70 - (70 + 620 + 22)
    sy = y + 56 + 90
    sh_ = 430
    rr(d, [sx, sy, sx + sw, sy + sh_], 18, fill=NAVY)
    eyebrow(d, (sx + 26, sy + 28), "Certified copies used", 12, GOLD_SOFT)
    d.text((sx + 26, sy + 58), "11", font=F("serif", 64), fill=PAPER)
    d.text((sx + 26 + tw(d, "11", F("serif", 64)) + 8, sy + 86), "/ 15", font=F("serif", 34), fill=alpha_on(PAPER, NAVY, 0.5))
    by = sy + 160
    rr(d, [sx + 26, by, sx + sw - 26, by + 10], 5, fill=alpha_on(PAPER, NAVY, 0.18))
    rr(d, [sx + 26, by, sx + 26 + (sw - 52) * 0.73, by + 10], 5, fill=GOLD_SOFT)
    para(d, (sx + 26, by + 26), "Reorder before you hit zero — running out stalls everything for weeks.", F("sans", 15), alpha_on(PAPER, NAVY, 0.7), sw - 52, 22)
    return img


def card09():
    img, d = shell(PAPER)
    card_top(d, 9)
    y = headline(d, 132, "One purchase · two formats", ["Excel and Google Sheets.", "Both included."], 58)
    y = para(d, (70, y + 14), "Most sellers split these into two listings and charge you twice. Here, the same workbook opens natively in Excel and uploads cleanly to Google Sheets — every formula intact.", F("sans", 23), INK70, 740, 33)

    def frame(cx, cy, wdt, chrome, badge, accent):
        ht = 44 + 30 + 7 * 44
        rr(d, [cx, cy, cx + wdt, cy + ht], 16, fill=WHITE, outline=LINE_SOFT, width=1)
        for i, c in enumerate([(230, 163, 154), (232, 207, 143), (169, 205, 170)]):
            d.ellipse([cx + 16 + i * 21, cy + 17, cx + 27 + i * 21, cy + 28], fill=c)
        d.text((cx + 86, cy + 14), chrome, font=F("mono", 12), fill=INK55)
        d.line([(cx, cy + 44), (cx + wdt, cy + 44)], fill=LINE, width=1)
        d.rectangle([cx + 1, cy + 45, cx + wdt - 1, cy + 74], fill=accent)
        d.text((cx + 16, cy + 51), badge, font=F("sans7", 13), fill=(255, 255, 255))
        for i in range(7):
            ry = cy + 74 + i * 44
            if i % 2:
                d.rectangle([cx + 1, ry, cx + wdt - 1, ry + 44], fill=alpha_on(PAPER2, WHITE, 0.5))
            d.rectangle([cx + 16, ry + 17, cx + 16 + wdt * 0.4, ry + 27], fill=LINE)
            d.rectangle([cx + 28 + wdt * 0.4, ry + 17, cx + 28 + wdt * 0.76, ry + 27], fill=LINE_SOFT)
            d.rectangle([cx + wdt - 56, ry + 17, cx + wdt - 16, ry + 27], fill=accent if i < 4 else GOLD_PALE)
            d.line([(cx + 1, ry + 44), (cx + wdt - 1, ry + 44)], fill=LINE_SOFT, width=1)
        return ht

    fw = (W - 140 - 80) // 2
    fy = y + 150
    frame(70, fy, fw, "Executor_Estate_Kit.xlsx", "MICROSOFT EXCEL", (58, 113, 80))
    d.text((70 + fw + 28, fy + 190), "+", font=F("serif", 40), fill=INK40)
    frame(70 + fw + 80, fy, fw, "sheets.google.com", "GOOGLE SHEETS", (47, 125, 90))
    pt = "Free to upload · all formulas work in both"
    f = F("sans6", 18)
    pw = tw(d, pt, f) + 78
    px = (W - pw) / 2
    py = H - 150
    rr(d, [px, py, px + pw, py + 52], 26, fill=SAGE)
    d.line([(px + 26, py + 26), (px + 31, py + 32), (px + 41, py + 20)], fill=SAGE_INK, width=3, joint="curve")
    d.text((px + 56, py + 13), pt, font=f, fill=SAGE_INK)
    return img


def card10():
    img, d = shell(PAPER2)
    card_top(d, 10)
    y = headline(d, 130, "Why this one", ["Built with a finance background,", "for real executors."], 54)
    steps = [("1", "Purchase", "Instant download — no physical item ships."),
             ("2", "Open it your way", "Use in Excel, or upload to Google Sheets (free)."),
             ("3", "Start with the guide", "Then the First 30 Days tab. The workbook organizes the rest.")]
    y += 32
    cw = (W - 140 - 32) // 3
    for i, (n, t, ds) in enumerate(steps):
        cx = 70 + i * (cw + 16)
        rr(d, [cx, y, cx + cw, y + 210], 16, fill=WHITE)
        rr(d, [cx + 24, y + 24, cx + 64, y + 64], 11, fill=NAVY)
        d.text((cx + 38, y + 28), n, font=F("serif6", 22), fill=GOLD_SOFT)
        d.text((cx + 24, y + 84), t, font=F("sans7", 21), fill=NAVY)
        para(d, (cx + 24, y + 118), ds, F("sans", 16), ink(WHITE, 0.55), cw - 48, 23)
    # image slot placeholder
    py0, py1 = y + 236, H - 320
    slot = Image.new("RGB", (W - 140, py1 - py0), PAPER2)
    sd = ImageDraw.Draw(slot)
    for k in range(-slot.height, slot.width, 20):
        sd.line([(k, slot.height), (k + slot.height, 0)], fill=alpha_on(NAVY, PAPER2, 0.05), width=10)
    m = Image.new("L", slot.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, slot.width, slot.height], radius=18, fill=255)
    img.paste(slot, (70, py0), m)
    dd = ImageDraw.Draw(img)
    rr(dd, [70, py0, W - 70, py1], 18, outline=alpha_on(NAVY, PAPER2, 0.22), width=2)
    ph = "YOUR PHOTO — sunlit desk, hands & notebook"
    f = F("mono", 12)
    dd.text(((W - tw(dd, ph, f)) / 2, (py0 + py1) / 2 - 8), ph, font=f, fill=ink(PAPER2, 0.55))
    yb = py1 + 26
    d.line([(70, yb), (W - 70, yb)], fill=LINE, width=1)
    stars(d, 70, yb + 22)
    d.text((70, yb + 56), "“Calmly. Completely. In the order that matters.”", font=F("serif", 27), fill=NAVY)
    para(d, (70, yb + 104), "An organizational tool, not legal or tax advice — rules vary by state. Designed to keep you so organized that when you do need an attorney or CPA, they bill fewer hours.", F("sans", 13), ink(PAPER2, 0.40), 620, 18)
    wordmark(d, W - 70 - 230, yb + 70, 18)
    return img


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card01, card02, card03, card04, card05, card06, card07, card08, card09, card10], 1):
        im = fn()
        path = os.path.join(OUT, f"listing-{i:02d}.png")
        im.save(path, optimize=True)
        print(f"wrote {path}")
