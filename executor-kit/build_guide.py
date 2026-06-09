#!/usr/bin/env python3
"""Generates The_Executors_First_30_Days.pdf — the companion guide to the workbook."""

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (HRFlowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer)

NAVY = HexColor("#1F3A5F")
GOLD = HexColor("#C9A227")
GREY = HexColor("#555555")

styles = {
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=26, leading=32, textColor=NAVY, alignment=TA_CENTER, spaceAfter=8),
    "subtitle": ParagraphStyle("subtitle", fontName="Helvetica-Oblique", fontSize=13, leading=18, textColor=GREY, alignment=TA_CENTER, spaceAfter=24),
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=NAVY, spaceBefore=18, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=12, leading=16, textColor=GOLD, spaceBefore=12, spaceAfter=4),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10.5, leading=15.5, spaceAfter=8),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=10.5, leading=15.5, spaceAfter=5, leftIndent=18, bulletIndent=6),
    "note": ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=9, leading=13, textColor=GREY, spaceBefore=12),
}


def p(text, style="body"):
    return Paragraph(text, styles[style])


def b(text):
    return Paragraph(text, styles["bullet"], bulletText="•")


doc = SimpleDocTemplate(
    "/home/user/hello-world/executor-kit/The_Executors_First_30_Days.pdf",
    pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
    topMargin=0.9 * inch, bottomMargin=0.9 * inch,
    title="The Executor's First 30 Days", author="Executor & Estate Settlement Kit",
)

story = [
    Spacer(1, 1.6 * inch),
    p("The Executor's<br/>First 30 Days", "title"),
    p("A calm, step-by-step guide for the person<br/>who has just been handed the hardest job nobody trains you for.", "subtitle"),
    HRFlowable(width="40%", thickness=1.5, color=GOLD, spaceAfter=24),
    p("Companion guide to the Executor &amp; Estate Settlement Workbook", "subtitle"),
    PageBreak(),

    p("Start here: you don't have to do everything today", "h1"),
    p("If you are reading this, you have probably just lost someone — and on top of grieving, you have been "
      "made responsible for their affairs. The job feels enormous because nobody can see its edges: bills are "
      "arriving, family members are asking questions, and every institution seems to want something different."),
    p("Here is the truth that makes this manageable: <b>estate settlement is a sequence, not a pile.</b> "
      "A small number of things are genuinely urgent in the first week. Most of the rest waits politely "
      "until the court appoints you. This guide walks the sequence in order, and the workbook gives every "
      "piece of information a place to live, so nothing depends on your memory during the worst month to rely on it."),

    p("Three rules before anything else", "h1"),
    p("Almost every serious, personally costly executor mistake is a violation of one of these three rules. "
      "Read them now, and re-read them any time you feel pressured."),
    p("Rule 1 — Never mix estate money with your own.", "h2"),
    p("Do not pay estate bills from your personal account, and do not deposit estate money into it — even "
      "temporarily, even with perfect intentions. Commingling funds is the fastest way for an executor to "
      "become personally liable. If you must pay something urgent before the estate account exists (a funeral "
      "deposit, for example), keep the receipt and record it in the workbook's Estate Ledger as an executor "
      "expense to be reimbursed."),
    p("Rule 2 — Distribute nothing until debts and taxes are settled.", "h2"),
    p("Family members may ask for items or money early, and the pressure can be intense. But debts and taxes "
      "are paid first by law, and if you distribute assets and the money later runs short, the difference can "
      "come out of your pocket. “The court requires me to settle debts and taxes first” is a complete, "
      "kind, and true answer."),
    p("Rule 3 — Write everything down.", "h2"),
    p("Every call, every letter, every dollar. Beneficiaries are legally entitled to an accounting of what you "
      "did, and months of small decisions are impossible to reconstruct from memory. The Task Log and Estate "
      "Ledger tabs exist precisely for this. Five minutes of logging per action is the cheapest insurance you "
      "will ever buy."),
    PageBreak(),

    p("Week 1 — Protect and gather", "h1"),
    p("Nothing this week requires court authority. The goal is simply to secure what exists and find the documents that control everything else."),
    b("<b>Find the original will.</b> Check the safe, filing cabinet, desk drawers, and ask their attorney. Many wills sit in bank safe-deposit boxes — access rules vary by state, so ask the bank what they require."),
    b("<b>Order 10–15 certified copies of the death certificate</b> from the funeral home or vital records office. Nearly every institution demands its own certified copy, and running out mid-process stalls everything for weeks. The workbook's Notifications tab tracks where each copy goes."),
    b("<b>Secure the property.</b> Lock the home, garage and vehicles; consider re-keying if many people have keys. From now on, you are responsible for protecting these assets."),
    b("<b>Arrange care for dependents and pets.</b> Welfare before paperwork, always."),
    b("<b>Forward the mail</b> at usps.com. Incoming mail is your single best discovery tool — it will surface accounts, debts, and subscriptions no one knew about."),
    b("<b>Start the Document Locator tab</b> as papers surface. You are not organizing yet — just recording where things are."),

    p("Week 2 — Get appointed and get the estate its own identity", "h1"),
    p("This week converts you from “family member” to “legal representative.” Until these steps are done, institutions are not allowed to deal with you."),
    b("<b>File the will and a petition for probate</b> with the county court where they lived. Call the probate clerk first and ask exactly what your county requires — clerks answer these questions all day and most are genuinely helpful."),
    b("<b>Receive your Letters Testamentary</b> (or Letters of Administration). This document is your legal authority; get several certified copies."),
    b("<b>Get an EIN for the estate</b> at irs.gov. It is free and takes about ten minutes online. The estate is its own taxpayer and cannot use the deceased's Social Security number."),
    b("<b>Open an estate checking account</b> using the EIN and your Letters. From today, every dollar in or out of the estate flows through this one account — and into the Estate Ledger tab."),

    p("Weeks 2–3 — Notify", "h1"),
    p("Work through the Notifications tab. The most important calls:"),
    b("<b>Social Security Administration</b> — benefits must stop (and survivor benefits may start)."),
    b("<b>Employer</b> — final pay, life insurance through work, retirement plans."),
    b("<b>Life insurers</b> — claims usually need only a certified death certificate and a claim form; proceeds typically pass outside the estate to named beneficiaries."),
    b("<b>Banks and brokerages</b> — accounts are frozen or retitled to the estate."),
    b("<b>The three credit bureaus</b> — flag the file as deceased and request a credit report. This prevents identity theft and is your best map of unknown accounts and debts."),
    PageBreak(),

    p("Weeks 3–4 — Inventory and triage", "h1"),
    b("<b>Build the asset inventory</b> in the Assets tab, valuing everything as of the date of death. These numbers become the court's inventory filing and the opening balance of your final accounting. Real estate and valuables may need a professional appraisal — the estate pays for it."),
    b("<b>List every debt in the Debts tab, but pay nothing yet.</b> Verify each claim, then confirm the order of payment — debts have a legal priority sequence, and if the estate might not cover everything, paying the wrong creditor first can create personal liability. This is a moment where a short consultation with a probate attorney earns its fee."),
    b("<b>Cancel subscriptions and services</b> using the Services tab. Every forgotten month drains the estate."),
    b("<b>Put the tax deadlines on your calendar:</b> the final personal income tax return (Form 1040) and, if the estate earns income during administration, the estate income tax return (Form 1041)."),

    p("The five mistakes that cost executors personally", "h1"),
    b("<b>Commingling funds</b> — Rule 1. The most common and most punished mistake."),
    b("<b>Distributing too early</b> — Rule 2. Generosity now can become personal liability later."),
    b("<b>Too few death certificates</b> — order 10–15 up front; reorder the moment you run low."),
    b("<b>Missing tax deadlines</b> — penalties come from the estate, and sometimes from the executor."),
    b("<b>Thin records</b> — a beneficiary dispute two years from now is won or lost on the log you keep today."),

    p("When to get professional help", "h1"),
    p("Hiring help is not failure — it is what careful executors do, and <b>reasonable professional fees are paid "
      "by the estate, not by you.</b> Bring in a probate attorney when there is a dispute among beneficiaries, "
      "an insolvent or complex estate, a business to wind down, or real estate in multiple states. Bring in a "
      "CPA for the final 1040 and any 1041. For everything routine in between, the workbook keeps you organized "
      "enough that professionals bill fewer hours when you do use them."),

    p("How the workbook fits together", "h1"),
    p("Tabs flow in the order of the job: <b>First 30 Days</b> tells you what to do, <b>Task Log</b> records that "
      "you did it, <b>Documents / Notifications</b> capture the gathering phase, <b>Assets / Debts / Services</b> "
      "hold the inventory, <b>Estate Ledger</b> tracks every dollar of administration, <b>Distributions</b> "
      "records who received what, and <b>Final Accounting</b> assembles it all automatically into the summary "
      "courts and beneficiaries expect: beginning inventory, plus receipts, less disbursements, less "
      "distributions, equals remaining balance. Fill in the tabs as you go, and the hardest report of the whole "
      "process writes itself."),
    Spacer(1, 0.3 * inch),
    HRFlowable(width="100%", thickness=0.75, color=GOLD),
    p("This guide and workbook are organizational tools, not legal, tax, or financial advice. Probate rules vary "
      "by state and country. Confirm requirements with your probate court or a licensed professional. "
      "© 2026. For personal use by the purchaser; resale or redistribution is not permitted.", "note"),
]

doc.build(story)
print("Guide PDF written.")
