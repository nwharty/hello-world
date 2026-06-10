#!/usr/bin/env python3
"""Generates The_Executors_First_30_Days.pdf — the companion guide.

Design per the Executor Kit handoff: navy gradient cover with double brass
keyline, Spectral/Hanken Grotesk/Spline Sans Mono type, brass eyebrows,
sage callouts, mono folios in alternating corners.
"""

import os

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (HRFlowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle)

NAVY = HexColor("#223A52")
NAVY_G1 = HexColor("#27425D")
NAVY_G2 = HexColor("#172838")
PAPER = HexColor("#FAF7F1")
SAGE = HexColor("#E7EFE5")
SAGE_INK = HexColor("#4A6450")
GOLD = HexColor("#B58A34")
GOLD_SOFT = HexColor("#D4B164")
INK_70 = Color(34 / 255, 58 / 255, 82 / 255, alpha=0.70)
INK_55 = Color(34 / 255, 58 / 255, 82 / 255, alpha=0.55)
INK_40 = Color(34 / 255, 58 / 255, 82 / 255, alpha=0.40)

FONTDIR = "/tmp/fonts"
FONTS = {
    "Spectral": "Spectral-500.ttf",
    "Spectral-SB": "Spectral-600.ttf",
    "Hanken": "Hanken-400.ttf",
    "Hanken-Bold": "Hanken-700.ttf",
    "Mono": "SplineMono-500.ttf",
}
have_brand_fonts = all(os.path.exists(os.path.join(FONTDIR, f)) for f in FONTS.values())
if have_brand_fonts:
    for name, fn in FONTS.items():
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONTDIR, fn)))
    SERIF, SERIF_SB, SANS, SANS_B, MONO = "Spectral", "Spectral-SB", "Hanken", "Hanken-Bold", "Mono"
else:  # graceful fallback if fonts were not downloaded
    SERIF, SERIF_SB, SANS, SANS_B, MONO = "Times-Roman", "Times-Bold", "Helvetica", "Helvetica-Bold", "Courier"

W, H = letter
TITLE = "The Executor's First 30 Days"


def tracked(s):
    return " ".join(list(s.upper()))


styles = {
    "eyebrow": ParagraphStyle("eyebrow", fontName=MONO, fontSize=9, leading=13, textColor=GOLD, spaceBefore=16, spaceAfter=6),
    "h1": ParagraphStyle("h1", fontName=SERIF, fontSize=21, leading=25, textColor=NAVY, spaceAfter=10),
    "body": ParagraphStyle("body", fontName=SANS, fontSize=10.5, leading=16.5, textColor=INK_70, spaceAfter=8),
    "bullet": ParagraphStyle("bullet", fontName=SANS, fontSize=10.5, leading=16, textColor=INK_70, spaceAfter=6,
                             leftIndent=20, bulletIndent=4, bulletFontName=SANS_B, bulletColor=SAGE_INK),
    "rule_t": ParagraphStyle("rule_t", fontName=SANS_B, fontSize=11.5, leading=15, textColor=NAVY, spaceBefore=10, spaceAfter=2),
    "rule_b": ParagraphStyle("rule_b", fontName=SANS, fontSize=10, leading=15, textColor=INK_55, spaceAfter=6, leftIndent=0),
    "note": ParagraphStyle("note", fontName=SANS, fontSize=8.5, leading=12.5, textColor=INK_40, spaceBefore=12),
    "callout": ParagraphStyle("callout", fontName=SANS, fontSize=10, leading=15.5, textColor=SAGE_INK),
}


def p(text, style="body"):
    return Paragraph(text, styles[style])


def eyebrow(text):
    return Paragraph(tracked(text), styles["eyebrow"])


def b(text):
    return Paragraph(text, styles["bullet"], bulletText="✓")


def numbered(n, title, body):
    return Paragraph(
        f'<font name="{SERIF}" color="#B58A34" size="14">{n}</font>'
        f'&nbsp;&nbsp;<font name="{SANS_B}" color="#223A52" size="11.5">{title}</font>'
        f'<br/><font size="10" color="#5A6B7C">{body}</font>',
        ParagraphStyle("num", fontName=SANS, fontSize=10.5, leading=15.5, spaceAfter=10, leftIndent=24, firstLineIndent=-24),
    )


def callout(text):
    t = Table([[Paragraph(text, styles["callout"])]], colWidths=[W - 2 * 0.95 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SAGE),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    return t


def draw_mark(canv, cx, cy, r):
    canv.saveState()
    canv.setFillColor(NAVY)
    canv.circle(cx, cy, r, stroke=0, fill=1)
    canv.setStrokeColor(Color(212 / 255, 177 / 255, 100 / 255, alpha=0.5))
    canv.setLineWidth(1.2)
    canv.circle(cx, cy, r - 1.5, stroke=1, fill=0)
    s = r * 0.62
    canv.setFillColor(GOLD_SOFT)
    pth = canv.beginPath()
    pts = [(0, s), (0.2 * s, 0.2 * s), (s, 0), (0.2 * s, -0.2 * s), (0, -s), (-0.2 * s, -0.2 * s), (-s, 0), (-0.2 * s, 0.2 * s)]
    pth.moveTo(cx + pts[0][0], cy + pts[0][1])
    for x, y in pts[1:]:
        pth.lineTo(cx + x, cy + y)
    pth.close()
    canv.drawPath(pth, stroke=0, fill=1)
    canv.restoreState()


def draw_cover(canv, doc):
    canv.saveState()
    try:
        canv.linearGradient(0, H, W, 0, (NAVY_G1, NAVY_G2), extend=False)
    except Exception:
        canv.setFillColor(NAVY_G2)
        canv.rect(0, 0, W, H, stroke=0, fill=1)
    # double brass keyline
    canv.setLineWidth(4.5)
    canv.setStrokeColor(Color(212 / 255, 177 / 255, 100 / 255, alpha=0.10))
    canv.roundRect(20, 20, W - 40, H - 40, 6, stroke=1, fill=0)
    canv.setLineWidth(1)
    canv.setStrokeColor(Color(212 / 255, 177 / 255, 100 / 255, alpha=0.40))
    canv.roundRect(26, 26, W - 52, H - 52, 5, stroke=1, fill=0)

    draw_mark(canv, 78, H - 80, 21)
    canv.setFont(MONO, 9)
    canv.setFillColor(Color(250 / 255, 247 / 255, 241 / 255, alpha=0.55))
    canv.drawRightString(W - 54, H - 84, tracked("PDF Guide"))

    y = 320
    canv.setFont(MONO, 9.5)
    canv.setFillColor(GOLD_SOFT)
    canv.drawString(64, y + 96, tracked("The companion guide"))
    canv.setFillColor(PAPER)
    canv.setFont(SERIF, 40)
    canv.drawString(62, y + 46, "The Executor's")
    canv.drawString(62, y, "First 30 Days")
    canv.setFillColor(GOLD)
    canv.roundRect(64, y - 26, 48, 2.2, 1, stroke=0, fill=1)
    canv.setFont(SANS, 13)
    canv.setFillColor(Color(250 / 255, 247 / 255, 241 / 255, alpha=0.74))
    for i, line in enumerate([
        "A calm, step-by-step guide for the person who has just",
        "been handed the hardest job nobody trains you for.",
    ]):
        canv.drawString(64, y - 56 - i * 19, line)
    canv.setFont(SANS, 10)
    canv.setFillColor(Color(250 / 255, 247 / 255, 241 / 255, alpha=0.5))
    canv.drawString(64, 56, "Companion to the 12-tab Estate Workbook")
    canv.restoreState()


def draw_folio(canv, doc):
    n = canv.getPageNumber() - 1  # interior numbering starts at 1
    canv.saveState()
    canv.setFont(MONO, 8.5)
    canv.setFillColor(INK_40)
    if n % 2 == 0:
        canv.drawRightString(W - 0.95 * inch, 0.55 * inch, f"{TITLE} — {n}")
    else:
        canv.drawString(0.95 * inch, 0.55 * inch, f"{n} — {TITLE}")
    canv.restoreState()


doc = SimpleDocTemplate(
    "/home/user/hello-world/executor-kit/The_Executors_First_30_Days.pdf",
    pagesize=letter, leftMargin=0.95 * inch, rightMargin=0.95 * inch,
    topMargin=0.85 * inch, bottomMargin=0.9 * inch,
    title=TITLE, author="The Executor Kit",
)

story = [
    Spacer(1, 1),
    PageBreak(),

    eyebrow("Start here"),
    p("You don't have to do everything today", "h1"),
    p("If you are reading this, you have probably just lost someone — and on top of grieving, you have been "
      "made responsible for their affairs. The job feels enormous because nobody can see its edges: bills are "
      "arriving, family members are asking questions, and every institution seems to want something different."),
    p("Here is the truth that makes this manageable: <b>estate settlement is a sequence, not a pile.</b> "
      "A small number of things are genuinely urgent in the first week. Most of the rest waits politely "
      "until the court appoints you. This guide walks the sequence in order, and the workbook gives every "
      "piece of information a place to live, so nothing depends on your memory during the worst month to rely on it."),

    eyebrow("Before anything else"),
    p("Three rules before you do anything", "h1"),
    p("Almost every serious, personally costly executor mistake is a violation of one of these three rules. "
      "Read them now, and re-read them any time you feel pressured."),
    numbered(1, "Never mix estate money with your own.",
             "Do not pay estate bills from your personal account, and do not deposit estate money into it — even "
             "temporarily, even with perfect intentions. Commingling funds is the fastest way for an executor to "
             "become personally liable. If you must pay something urgent before the estate account exists (a funeral "
             "deposit, for example), keep the receipt and record it in the Estate Ledger as an executor expense to be reimbursed."),
    numbered(2, "Distribute nothing until debts and taxes are settled.",
             "Family members may ask for items or money early, and the pressure can be intense. But debts and taxes "
             "are paid first by law, and if you distribute assets and the money later runs short, the difference can "
             "come out of your pocket. “The court requires me to settle debts and taxes first” is a complete, "
             "kind, and true answer."),
    numbered(3, "Write everything down.",
             "Every call, every letter, every dollar. Beneficiaries are legally entitled to an accounting of what you "
             "did, and months of small decisions are impossible to reconstruct from memory. The Task Log and Estate "
             "Ledger tabs exist precisely for this. Five minutes of logging per action is the cheapest insurance you "
             "will ever buy."),
    PageBreak(),

    eyebrow("Week 1 · Protect and gather"),
    p("Nothing this week needs the court", "h1"),
    p("The goal is simply to secure what exists and find the documents that control everything else."),
    b("<b>Find the original will.</b> Check the safe, filing cabinet, desk drawers, and ask their attorney. Many wills sit in bank safe-deposit boxes — access rules vary by state, so ask the bank what they require."),
    b("<b>Order 10–15 certified copies of the death certificate</b> from the funeral home or vital records office. Nearly every institution demands its own certified copy, and running out mid-process stalls everything for weeks. The workbook's Notifications tab tracks where each copy goes."),
    b("<b>Secure the property.</b> Lock the home, garage and vehicles; consider re-keying if many people have keys. From now on, you are responsible for protecting these assets."),
    b("<b>Arrange care for dependents and pets.</b> Welfare before paperwork, always."),
    b("<b>Forward the mail</b> at usps.com. Incoming mail is your single best discovery tool — it will surface accounts, debts, and subscriptions no one knew about."),
    b("<b>Start the Document Locator tab</b> as papers surface. You are not organizing yet — just recording where things are."),
    callout("<b>The truth that makes this manageable:</b> estate settlement is a sequence, not a pile. "
            "A few things are genuinely urgent. Most of the rest waits politely until the court appoints you."),

    eyebrow("Week 2 · Get appointed"),
    p("Give the estate its own identity", "h1"),
    p("This week converts you from “family member” to “legal representative.” Until these steps are done, institutions are not allowed to deal with you."),
    b("<b>File the will and a petition for probate</b> with the county court where they lived. Call the probate clerk first and ask exactly what your county requires — clerks answer these questions all day and most are genuinely helpful."),
    b("<b>Receive your Letters Testamentary</b> (or Letters of Administration). This document is your legal authority; get several certified copies."),
    b("<b>Get an EIN for the estate</b> at irs.gov. It is free and takes about ten minutes online. The estate is its own taxpayer and cannot use the deceased's Social Security number."),
    b("<b>Open an estate checking account</b> using the EIN and your Letters. From today, every dollar in or out of the estate flows through this one account — and into the Estate Ledger tab."),
    PageBreak(),

    eyebrow("Weeks 2–3 · Notify"),
    p("Make the calls, in order", "h1"),
    p("Work through the Notifications tab. The most important calls:"),
    b("<b>Social Security Administration</b> — benefits must stop (and survivor benefits may start)."),
    b("<b>Employer</b> — final pay, life insurance through work, retirement plans."),
    b("<b>Life insurers</b> — claims usually need only a certified death certificate and a claim form; proceeds typically pass outside the estate to named beneficiaries."),
    b("<b>Banks and brokerages</b> — accounts are frozen or retitled to the estate."),
    b("<b>The three credit bureaus</b> — flag the file as deceased and request a credit report. This prevents identity theft and is your best map of unknown accounts and debts."),

    eyebrow("Weeks 3–4 · Inventory and triage"),
    p("Build the numbers everything rests on", "h1"),
    b("<b>Build the asset inventory</b> in the Assets tab, valuing everything as of the date of death. These numbers become the court's inventory filing and the opening balance of your final accounting. Real estate and valuables may need a professional appraisal — the estate pays for it."),
    b("<b>List every debt in the Debts tab, but pay nothing yet.</b> Verify each claim, then confirm the order of payment — debts have a legal priority sequence, and if the estate might not cover everything, paying the wrong creditor first can create personal liability. This is a moment where a short consultation with a probate attorney earns its fee."),
    b("<b>Cancel subscriptions and services</b> using the Services tab. Every forgotten month drains the estate."),
    b("<b>Put the tax deadlines on your calendar:</b> the final personal income tax return (Form 1040) and, if the estate earns income during administration, the estate income tax return (Form 1041)."),
    PageBreak(),

    eyebrow("Protect yourself"),
    p("The five mistakes that cost executors personally", "h1"),
    numbered(1, "Commingling funds", "Rule 1. The most common and most punished mistake."),
    numbered(2, "Distributing too early", "Rule 2. Generosity now can become personal liability later."),
    numbered(3, "Too few death certificates", "Order 10–15 up front; reorder the moment you run low."),
    numbered(4, "Missing tax deadlines", "Penalties come from the estate, and sometimes from the executor."),
    numbered(5, "Thin records", "A beneficiary dispute two years from now is won or lost on the log you keep today."),

    eyebrow("When to get help"),
    p("Hiring help is not failure", "h1"),
    p("It is what careful executors do, and <b>reasonable professional fees are paid by the estate, not by you.</b> "
      "Bring in a probate attorney when there is a dispute among beneficiaries, an insolvent or complex estate, a "
      "business to wind down, or real estate in multiple states. Bring in a CPA for the final 1040 and any 1041. "
      "For everything routine in between, the workbook keeps you organized enough that professionals bill fewer "
      "hours when you do use them."),

    eyebrow("The system"),
    p("How the workbook fits together", "h1"),
    p("Tabs flow in the order of the job: <b>First 30 Days</b> tells you what to do, <b>Task Log</b> records that "
      "you did it, <b>Documents / Notifications</b> capture the gathering phase, <b>Assets / Debts / Services</b> "
      "hold the inventory, <b>Estate Ledger</b> tracks every dollar of administration, <b>Distributions</b> "
      "records who received what, and <b>Final Accounting</b> assembles it all automatically into the summary "
      "courts and beneficiaries expect: beginning inventory, plus receipts, less disbursements, less "
      "distributions, equals remaining balance. Fill in the tabs as you go, and the hardest report of the whole "
      "process writes itself."),
    Spacer(1, 0.25 * inch),
    HRFlowable(width="100%", thickness=0.75, color=GOLD),
    p("This guide and workbook are organizational tools, not legal, tax, or financial advice. Probate rules vary "
      "by state and country. Confirm requirements with your probate court or a licensed professional. "
      "© 2026 The Executor Kit. For personal use by the purchaser; resale or redistribution is not permitted.", "note"),
]

doc.build(story, onFirstPage=draw_cover, onLaterPages=draw_folio)
print("Guide PDF written.")
