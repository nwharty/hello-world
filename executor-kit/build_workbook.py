#!/usr/bin/env python3
"""Generates Executor_Estate_Kit.xlsx — a 12-tab estate administration workbook.

The same .xlsx uploads cleanly to Google Sheets (File > Import), so one build
serves both formats sold in the Etsy listing.
"""

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

NAVY = "1F3A5F"
SAGE = "E8EFE5"
GOLD = "C9A227"
LIGHT = "F4F6F8"

HEADER_FONT = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
HEADER_FILL = PatternFill("solid", fgColor=NAVY)
TITLE_FONT = Font(name="Calibri", bold=True, size=16, color=NAVY)
SUB_FONT = Font(name="Calibri", size=11, italic=True, color="555555")
SECTION_FONT = Font(name="Calibri", bold=True, size=12, color=NAVY)
THIN = Side(style="thin", color="CCCCCC")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
MONEY = '"$"#,##0.00'

DISCLAIMER = (
    "This workbook is an organizational tool, not legal, tax, or financial advice. "
    "Estate and probate rules vary by state and country - confirm requirements with "
    "the probate court or a licensed professional."
)


def sheet_title(ws, title, subtitle, ncols):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncols)
    ws.cell(row=1, column=1, value=title).font = TITLE_FONT
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncols)
    ws.cell(row=2, column=1, value=subtitle).font = SUB_FONT
    ws.row_dimensions[1].height = 26


def header_row(ws, row, headers, widths):
    for i, (h, w) in enumerate(zip(headers, widths), start=1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = HEADER_FONT
        c.fill = HEADER_FILL
        c.alignment = Alignment(vertical="center", wrap_text=True)
        c.border = BORDER
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 28
    ws.freeze_panes = ws.cell(row=row + 1, column=1)


def blank_rows(ws, start, count, ncols, money_cols=(), date_cols=()):
    for r in range(start, start + count):
        for col in range(1, ncols + 1):
            c = ws.cell(row=r, column=col)
            c.border = BORDER
            if col in money_cols:
                c.number_format = MONEY
            if col in date_cols:
                c.number_format = "mm/dd/yyyy"
        if (r - start) % 2 == 1:
            for col in range(1, ncols + 1):
                ws.cell(row=r, column=col).fill = PatternFill("solid", fgColor=LIGHT)


def dropdown(ws, options, col_letter, first, last):
    dv = DataValidation(type="list", formula1='"' + ",".join(options) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"{col_letter}{first}:{col_letter}{last}")


STATUS = ["Not started", "In progress", "Done", "N/A"]

wb = Workbook()

# ---------------------------------------------------------------- Start Here
ws = wb.active
ws.title = "Start Here"
ws.sheet_properties.tabColor = GOLD
sheet_title(ws, "Executor & Estate Settlement Kit", "A calm, complete system for settling an estate - one tab at a time.", 2)
ws.column_dimensions["A"].width = 26
ws.column_dimensions["B"].width = 95

rows = [
    ("", ""),
    ("HOW TO USE THIS KIT", ""),
    ("1.", "Read the companion guide (The Executor's First 30 Days) before anything else. It tells you what is urgent and what can wait."),
    ("2.", "Work through the 'First 30 Days' tab. It is ordered by priority - you do not need to do everything at once."),
    ("3.", "Log every call, email, and letter in 'Task Log'. Months from now, this record protects you."),
    ("4.", "Record every asset, debt, and document as you discover them. Values can be added later."),
    ("5.", "Once the estate account is open, track every dollar in 'Estate Ledger'. The 'Final Accounting' tab totals everything automatically."),
    ("", ""),
    ("THE TABS", ""),
    ("First 30 Days", "Priority-ordered checklist for the critical first month."),
    ("Task Log", "Running log of every call, email, and letter."),
    ("Key Contacts", "Attorney, CPA, court clerk, institutions, beneficiaries."),
    ("Documents", "Where every important document is (or where you found it)."),
    ("Notifications", "Who must be notified, and where certified death certificates went."),
    ("Assets", "Full inventory with date-of-death values - the basis of the estate."),
    ("Debts", "Every claim and liability, verified before it is paid."),
    ("Services", "Subscriptions and utilities to cancel or transfer."),
    ("Estate Ledger", "Every dollar in and out of the estate account."),
    ("Distributions", "What each beneficiary receives, with signed-release tracking."),
    ("Final Accounting", "Automatic summary in the format probate courts expect."),
    ("", ""),
    ("GOOGLE SHEETS", "Upload this file at sheets.google.com via File > Import > Upload. All formulas work in Google Sheets."),
    ("", ""),
    ("PLEASE NOTE", DISCLAIMER),
]
r = 4
for label, text in rows:
    a = ws.cell(row=r, column=1, value=label)
    b = ws.cell(row=r, column=2, value=text)
    b.alignment = Alignment(wrap_text=True, vertical="top")
    if label.isupper() and label:
        a.font = SECTION_FONT
    else:
        a.font = Font(bold=True, color=NAVY)
    r += 1

# ------------------------------------------------------------- First 30 Days
ws = wb.create_sheet("First 30 Days")
ws.sheet_properties.tabColor = NAVY
sheet_title(ws, "The First 30 Days", "Work top to bottom. 'Done' and 'N/A' both count as finished.", 5)
header_row(ws, 4, ["Priority", "Task", "Why it matters", "Status", "Notes"], [10, 52, 52, 14, 30])

tasks = [
    ("Week 1", "Locate the original will (and any codicils)", "Check safe, filing cabinet, desk, attorney, bank safe-deposit box. The original is usually required by the court."),
    ("Week 1", "Order 10-15 certified copies of the death certificate", "Banks, insurers, and agencies each demand their own certified copy. Running out mid-process causes weeks of delay."),
    ("Week 1", "Secure the home, vehicles, and valuables", "You are responsible for protecting estate property from this point forward. Change locks if needed."),
    ("Week 1", "Arrange care for dependents and pets", "Immediate welfare comes before paperwork."),
    ("Week 1", "Forward mail (USPS) and collect incoming bills", "Mail reveals accounts, debts, and subscriptions you do not know about yet."),
    ("Week 1", "Do NOT pay estate bills from your own money, and do NOT distribute anything yet", "Commingling funds and early distributions are the two most common - and most personally costly - executor mistakes."),
    ("Week 2", "File the will and petition for probate with the county court", "Nothing official can happen until the court appoints you. Ask the clerk what your county requires."),
    ("Week 2", "Obtain Letters Testamentary / Letters of Administration", "This court document is your legal authority. Institutions will refuse to talk to you without it."),
    ("Week 2", "Get an EIN for the estate (irs.gov, free, ~10 minutes)", "The estate is its own taxpayer. You need an EIN before opening the estate bank account."),
    ("Week 2", "Open an estate checking account", "Every dollar in and out of the estate flows through this one account. Start the Estate Ledger tab the same day."),
    ("Week 2-3", "Notify Social Security, employer, insurers, and banks", "Use the Notifications tab. Benefits may need to be stopped or claimed; accounts must be frozen or retitled."),
    ("Week 2-3", "Notify the three credit bureaus and request a credit report", "Prevents identity theft and reveals unknown debts and accounts."),
    ("Week 3-4", "Begin the asset inventory with date-of-death values", "The court's inventory filing and the final accounting are both built on these numbers. Use the Assets tab."),
    ("Week 3-4", "Identify and verify all debts before paying anything", "Debts are paid in a legal order of priority. Paying the wrong ones first can make you personally liable."),
    ("Week 3-4", "Cancel or transfer subscriptions and services", "Use the Services tab. Every month of delay drains the estate."),
    ("Week 3-4", "Calendar the tax deadlines (final 1040, estate 1041)", "The final personal return and the estate income tax return have firm deadlines with penalties."),
    ("Ongoing", "Log every action in the Task Log; keep every receipt", "Beneficiaries are entitled to an accounting. A complete record is your best protection against disputes."),
    ("Ongoing", "Consider a probate attorney or CPA for anything unclear", "Reasonable professional fees are paid by the estate, not by you. Getting help is normal, not failure."),
]
r = 5
for phase, task, why in tasks:
    ws.cell(row=r, column=1, value=phase).border = BORDER
    c = ws.cell(row=r, column=2, value=task)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    c.border = BORDER
    c = ws.cell(row=r, column=3, value=why)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    c.font = Font(size=10, color="555555")
    c.border = BORDER
    ws.cell(row=r, column=4).border = BORDER
    ws.cell(row=r, column=5).border = BORDER
    ws.row_dimensions[r].height = 42
    r += 1
dropdown(ws, STATUS, "D", 5, r - 1)

# ------------------------------------------------------------------ Task Log
ws = wb.create_sheet("Task Log")
sheet_title(ws, "Task & Communication Log", "One row per call, email, or letter. This log is your protection.", 7)
header_row(ws, 4, ["Date", "Type", "Who / Organization", "Regarding", "Outcome", "Follow-up date", "Follow-up done?"], [13, 12, 26, 34, 34, 15, 15])
blank_rows(ws, 5, 120, 7, date_cols=(1, 6))
dropdown(ws, ["Call", "Email", "Letter", "In person", "Court filing", "Other"], "B", 5, 124)
dropdown(ws, ["Yes", "No", "N/A"], "G", 5, 124)

# -------------------------------------------------------------- Key Contacts
ws = wb.create_sheet("Key Contacts")
sheet_title(ws, "Key Contacts", "Everyone you will call more than once.", 6)
header_row(ws, 4, ["Role", "Name", "Organization", "Phone", "Email", "Notes / account or case #"], [24, 22, 26, 17, 28, 34])
roles = ["Probate attorney", "CPA / tax preparer", "Probate court clerk", "Funeral home", "Financial advisor",
         "Life insurance agent", "Realtor / appraiser", "Employer HR contact", "Beneficiary", "Beneficiary", "Beneficiary"]
r = 5
for role in roles:
    ws.cell(row=r, column=1, value=role).border = BORDER
    for col in range(2, 7):
        ws.cell(row=r, column=col).border = BORDER
    r += 1
blank_rows(ws, r, 25, 6)

# ----------------------------------------------------------------- Documents
ws = wb.create_sheet("Documents")
sheet_title(ws, "Document Locator", "Where every important paper lives. Fill in locations as you find them.", 5)
header_row(ws, 4, ["Document", "Located?", "Where it is / where found", "Original or copy?", "Notes"], [38, 12, 36, 16, 30])
docs = ["Original will / codicils", "Trust documents", "Death certificates (certified)", "Letters Testamentary",
        "Birth certificate", "Marriage certificate", "Social Security card", "Deeds to real estate",
        "Vehicle titles", "Bank statements", "Investment / brokerage statements", "Retirement account statements",
        "Life insurance policies", "Pension / annuity documents", "Last 3 years of tax returns",
        "Mortgage / loan documents", "Business ownership documents", "Safe-deposit box key & location",
        "Password list / digital accounts", "Prepaid funeral contract", "Military discharge (DD-214)"]
r = 5
for d in docs:
    ws.cell(row=r, column=1, value=d).border = BORDER
    for col in range(2, 6):
        ws.cell(row=r, column=col).border = BORDER
    r += 1
blank_rows(ws, r, 10, 5)
dropdown(ws, ["Yes", "No", "Searching"], "B", 5, r + 9)
dropdown(ws, ["Original", "Copy"], "D", 5, r + 9)

# ------------------------------------------------------------- Notifications
ws = wb.create_sheet("Notifications")
sheet_title(ws, "Notifications & Death Certificate Tracker", "Who must be told - and which ones need a certified death certificate.", 7)
header_row(ws, 4, ["Who to notify", "Certified copy required?", "Date notified", "Method", "Confirmed / reference #", "Cert. copies used", "Notes"], [34, 20, 14, 14, 24, 16, 28])
parties = ["Social Security Administration", "Employer / HR (final pay, benefits)", "Life insurance company",
           "Health insurance / Medicare", "Banks (each account)", "Brokerage / investment firms",
           "Retirement plan administrators", "Pension provider", "Mortgage company", "Credit card issuers",
           "Credit bureaus (Equifax, Experian, TransUnion)", "DMV (licenses, vehicle titles)", "Veterans Affairs (if applicable)",
           "Utility companies", "Landlord / HOA", "Post office (mail forwarding)"]
r = 5
for p in parties:
    ws.cell(row=r, column=1, value=p).border = BORDER
    for col in range(2, 8):
        ws.cell(row=r, column=col).border = BORDER
    ws.cell(row=r, column=3).number_format = "mm/dd/yyyy"
    r += 1
blank_rows(ws, r, 10, 7, date_cols=(3,))
last = r + 9
dropdown(ws, ["Yes", "No", "Unsure"], "B", 5, last)
dropdown(ws, ["Call", "Mail", "Online", "In person"], "D", 5, last)
ws.cell(row=last + 2, column=1, value="Certified copies used so far:").font = SECTION_FONT
c = ws.cell(row=last + 2, column=6, value=f"=SUM(F5:F{last})")
c.font = Font(bold=True)

# -------------------------------------------------------------------- Assets
ws = wb.create_sheet("Assets")
ws.sheet_properties.tabColor = GOLD
sheet_title(ws, "Asset Inventory", "Every asset, valued as of the date of death. This is the foundation of the inventory filing and final accounting.", 9)
header_row(ws, 4, ["Category", "Institution / Description", "Account # (last 4)", "How titled",
                   "Has named beneficiary?", "Value at date of death", "Current value", "Status", "Notes"],
           [22, 30, 14, 18, 18, 18, 18, 16, 28])
blank_rows(ws, 5, 60, 9, money_cols=(6, 7))
cats = ["Bank account", "Investment / brokerage", "Retirement (IRA/401k)", "Real estate", "Vehicle",
        "Life insurance", "Business interest", "Personal property", "Digital asset", "Other"]
dropdown(ws, cats, "A", 5, 64)
dropdown(ws, ["Sole name", "Joint", "In trust", "POD/TOD"], "D", 5, 64)
dropdown(ws, ["Yes", "No", "Unsure"], "E", 5, 64)
dropdown(ws, ["Located", "Valued", "Retitled", "Sold", "Distributed", "Closed"], "H", 5, 64)
ws.cell(row=66, column=5, value="TOTALS:").font = SECTION_FONT
for col in (6, 7):
    c = ws.cell(row=66, column=col, value=f"=SUM({get_column_letter(col)}5:{get_column_letter(col)}64)")
    c.number_format = MONEY
    c.font = Font(bold=True)
    c.fill = PatternFill("solid", fgColor=SAGE)

# --------------------------------------------------------------------- Debts
ws = wb.create_sheet("Debts")
sheet_title(ws, "Debts & Liabilities", "Verify every claim before paying. Debts are paid in a legal order of priority - ask the court or an attorney if assets may not cover them all.", 8)
header_row(ws, 4, ["Creditor", "Type", "Account # (last 4)", "Balance at death", "Verified?", "Amount paid", "Date paid", "Notes"],
           [28, 20, 14, 16, 12, 16, 13, 30])
blank_rows(ws, 5, 40, 8, money_cols=(4, 6), date_cols=(7,))
dropdown(ws, ["Mortgage", "Auto loan", "Credit card", "Medical", "Taxes", "Personal loan", "Utility", "Funeral", "Other"], "B", 5, 44)
dropdown(ws, ["Yes", "No", "Disputed"], "E", 5, 44)
ws.cell(row=46, column=3, value="TOTALS:").font = SECTION_FONT
for col in (4, 6):
    c = ws.cell(row=46, column=col, value=f"=SUM({get_column_letter(col)}5:{get_column_letter(col)}44)")
    c.number_format = MONEY
    c.font = Font(bold=True)
    c.fill = PatternFill("solid", fgColor=SAGE)

# ------------------------------------------------------------------ Services
ws = wb.create_sheet("Services")
sheet_title(ws, "Services & Subscriptions", "Every recurring charge to cancel or transfer. Check bank and card statements for the full list.", 7)
header_row(ws, 4, ["Service", "Account / login", "Monthly cost", "Action", "Date completed", "Refund due?", "Notes"],
           [28, 26, 14, 16, 15, 13, 30])
svcs = ["Electric / gas", "Water / sewer", "Internet / cable", "Cell phone", "Streaming services",
        "Newspaper / magazines", "Gym membership", "Insurance (auto/home)", "Amazon / shopping", "Cloud storage"]
r = 5
for s in svcs:
    ws.cell(row=r, column=1, value=s).border = BORDER
    for col in range(2, 8):
        ws.cell(row=r, column=col).border = BORDER
    ws.cell(row=r, column=3).number_format = MONEY
    ws.cell(row=r, column=5).number_format = "mm/dd/yyyy"
    r += 1
blank_rows(ws, r, 15, 7, money_cols=(3,), date_cols=(5,))
dropdown(ws, ["Cancel", "Transfer", "Keep (estate)", "Done"], "D", 5, r + 14)

# ------------------------------------------------------------- Estate Ledger
ws = wb.create_sheet("Estate Ledger")
ws.sheet_properties.tabColor = GOLD
sheet_title(ws, "Estate Ledger - Money In / Money Out", "Every transaction in the estate account. The Final Accounting tab totals this automatically.", 7)
header_row(ws, 4, ["Date", "Type", "Category", "Payer / Payee", "Amount", "Receipt kept?", "Notes"],
           [13, 16, 24, 28, 16, 13, 34])
blank_rows(ws, 5, 150, 7, money_cols=(5,), date_cols=(1,))
dropdown(ws, ["Receipt (money in)", "Disbursement (money out)"], "B", 5, 154)
dropdown(ws, ["Asset sale proceeds", "Interest / dividends", "Refunds", "Final paycheck", "Other income",
              "Funeral expense", "Court / filing fees", "Attorney / CPA fees", "Taxes paid", "Debt payment",
              "Property upkeep", "Executor expense", "Other expense"], "C", 5, 154)
dropdown(ws, ["Yes", "No"], "F", 5, 154)

# ------------------------------------------------------------- Distributions
ws = wb.create_sheet("Distributions")
sheet_title(ws, "Beneficiary Distributions", "Distribute only after debts and taxes are settled (or with court/attorney guidance). Get a signed receipt for everything.", 8)
header_row(ws, 4, ["Beneficiary", "Relationship", "Entitlement per will", "Asset / item distributed", "Value / amount", "Date", "Receipt or release signed?", "Notes"],
           [24, 16, 24, 28, 16, 13, 10, 28])
blank_rows(ws, 5, 40, 8, money_cols=(5,), date_cols=(6,))
dropdown(ws, ["Yes", "No", "Sent - awaiting"], "G", 5, 44)
ws.cell(row=46, column=4, value="TOTAL DISTRIBUTED:").font = SECTION_FONT
c = ws.cell(row=46, column=5, value="=SUM(E5:E44)")
c.number_format = MONEY
c.font = Font(bold=True)
c.fill = PatternFill("solid", fgColor=SAGE)

# ---------------------------------------------------------- Final Accounting
ws = wb.create_sheet("Final Accounting")
ws.sheet_properties.tabColor = "B00020"
sheet_title(ws, "Final Accounting Summary", "Calculated automatically from your other tabs - the structure courts and beneficiaries expect: what came in, what went out, what remains.", 3)
ws.column_dimensions["A"].width = 52
ws.column_dimensions["B"].width = 20
ws.column_dimensions["C"].width = 60

lines = [
    ("ESTATE AT A GLANCE", None, ""),
    ("Beginning inventory (assets at date-of-death value)", "=SUM(Assets!F5:F64)", "From the Assets tab"),
    ("Plus: receipts during administration", "=SUMIF('Estate Ledger'!B5:B154,\"Receipt (money in)\",'Estate Ledger'!E5:E154)", "From the Estate Ledger"),
    ("Less: disbursements during administration", "=SUMIF('Estate Ledger'!B5:B154,\"Disbursement (money out)\",'Estate Ledger'!E5:E154)", "From the Estate Ledger"),
    ("Less: distributions to beneficiaries", "=SUM(Distributions!E5:E44)", "From the Distributions tab"),
    ("REMAINING ESTATE BALANCE", "=B5+B6-B7-B8", "Should match the estate bank account when complete"),
    ("", None, ""),
    ("DEBTS", None, ""),
    ("Total debts identified", "=SUM(Debts!D5:D44)", "From the Debts tab"),
    ("Total debts paid", "=SUM(Debts!F5:F44)", "From the Debts tab"),
    ("Debts remaining", "=B12-B13", ""),
    ("", None, ""),
    ("CLOSING CHECKLIST", None, ""),
    ("All debts and taxes paid", "", "Mark Done when true"),
    ("Final tax returns filed (final 1040, estate 1041)", "", ""),
    ("All distributions made and releases signed", "", ""),
    ("Final accounting shared with beneficiaries / filed with court", "", ""),
    ("Estate bank account closed", "", ""),
]
r = 4
for label, formula, note in lines:
    a = ws.cell(row=r, column=1, value=label)
    if label.isupper() and label:
        a.font = SECTION_FONT
        a.fill = PatternFill("solid", fgColor=SAGE)
        ws.cell(row=r, column=2).fill = PatternFill("solid", fgColor=SAGE)
        ws.cell(row=r, column=3).fill = PatternFill("solid", fgColor=SAGE)
    if formula:
        b = ws.cell(row=r, column=2, value=formula)
        b.number_format = MONEY
        b.font = Font(bold=label.isupper() or label.startswith("REMAINING"))
    n = ws.cell(row=r, column=3, value=note)
    n.font = Font(size=10, italic=True, color="555555")
    r += 1
dropdown(ws, STATUS, "B", 18, 22)
ws.cell(row=r + 1, column=1, value=DISCLAIMER).font = Font(size=9, italic=True, color="888888")

wb.save("/home/user/hello-world/executor-kit/Executor_Estate_Kit.xlsx")
print("Workbook written.")
