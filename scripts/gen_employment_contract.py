#!/usr/bin/env python3
"""
Generate docs/employment-contract.pdf — 3-page Employment Contract
(Meridian Group Ltd / Employee)

Usage:
    python scripts/gen_employment_contract.py
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos
from pathlib import Path

OUTPUT = Path(__file__).parent.parent / "docs" / "employment-contract.pdf"
LH = 4.5    # standard line height mm
INDENT = 5  # sub-clause indent mm


class LegalPDF(FPDF):
    doc_title = ""

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(110, 110, 110)
            self.cell(0, 4, self.doc_title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")
            self.set_draw_color(200, 200, 200)
            self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
            self.ln(4)
            self.set_text_color(0, 0, 0)
            self.set_draw_color(0, 0, 0)

    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 4,
                  f"Page {self.page_no()} of {{nb}}  |  Prepared by Vantage Legal LLP  |  CONFIDENTIAL",
                  align="C")
        self.set_text_color(0, 0, 0)


def build():
    """Generate the employment contract PDF and write it to docs/employment-contract.pdf."""
    pdf = LegalPDF(orientation="P", unit="mm", format="LETTER")
    pdf.doc_title = "EMPLOYMENT CONTRACT  |  MERIDIAN GROUP LTD"
    pdf.alias_nb_pages()
    pdf.set_margins(25.4, 22, 25.4)
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    W = pdf.epw  # effective page width

    # ── helpers ──────────────────────────────────────────────────────────────

    def title_block(text):
        pdf.set_font("Helvetica", "B", 15)
        pdf.multi_cell(W, 8, text, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1)

    def subtitle(text):
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(W, 4.5, text, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

    def party_block(text):
        pdf.set_font("Helvetica", "B", 9)
        pdf.multi_cell(W, LH, text, align="J", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1)

    def center_line(text):
        pdf.set_font("Helvetica", "I", 9)
        pdf.multi_cell(W, LH, text, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(0.5)

    def recital(text):
        pdf.set_font("Helvetica", "I", 9)
        pdf.multi_cell(W, LH, text, align="J", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1.5)

    def rule():
        pdf.set_draw_color(190, 190, 190)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
        pdf.set_draw_color(0, 0, 0)
        pdf.ln(2.5)

    def clause_head(num, text):
        pdf.ln(1.5)
        pdf.set_font("Helvetica", "B", 10)
        pdf.multi_cell(W, LH, f"{num}.  {text}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(0.3)

    def sub(num, text):
        pdf.set_x(pdf.l_margin + INDENT)
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(W - INDENT, LH, f"{num}  {text}", align="J",
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1)

    def item(letter, text):
        pdf.set_x(pdf.l_margin + INDENT * 2)
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(W - INDENT * 2, LH, f"({letter})  {text}", align="J",
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(0.3)

    # ── TITLE ────────────────────────────────────────────────────────────────
    pdf.ln(2)
    title_block("EMPLOYMENT CONTRACT")
    subtitle("Commencement Date: March 4, 2024  |  Reference No. EMP-2024-0017")
    rule()

    # ── PARTIES ──────────────────────────────────────────────────────────────
    party_block(
        "EMPLOYER: MERIDIAN GROUP LTD, a Delaware limited liability company, 500 Delaware "
        "Avenue, Suite 1200, Wilmington, DE 19801 (\"Company\");"
    )
    center_line("and")
    party_block(
        "EMPLOYEE: Jordan A. Harwell, residing at 84 Chestnut Hill Road, Radnor, PA 19087 "
        "(\"Employee\")."
    )
    rule()

    recital(
        "The Company wishes to employ Employee on the terms set out below, and Employee "
        "accepts employment on those terms. Both Parties acknowledge receipt of adequate "
        "consideration and agree as follows:"
    )

    # ── 1. POSITION AND DUTIES ────────────────────────────────────────────────
    clause_head("1", "POSITION AND DUTIES")
    sub("1.1",
        "The Company employs Employee as Director of Enterprise Solutions, reporting to the "
        "Chief Operating Officer. Employee's primary work location is 500 Delaware Avenue, "
        "Suite 1200, Wilmington, DE 19801, subject to reasonable travel requirements.")
    sub("1.2",
        "Employee shall: (a) perform all duties assigned by the Company consistent with the "
        "role; (b) devote full business-time attention and best efforts to the Company's "
        "business; (c) comply with all Company policies and procedures as amended from time "
        "to time; and (d) promptly disclose to the Company any conflict of interest.")
    sub("1.3",
        "Employee shall not, during employment, hold any other paid position or directorship "
        "without prior written consent of the Chief Operating Officer, except for passive "
        "investments representing less than two percent (2%) of any publicly traded entity.")

    # ── 2. TERM ───────────────────────────────────────────────────────────────
    clause_head("2", "TERM")
    sub("2.1",
        "Employment commences on the Commencement Date and continues indefinitely until "
        "terminated in accordance with Section 8. This Agreement does not constitute a "
        "guarantee of employment for any fixed period.")

    # ── 3. COMPENSATION ───────────────────────────────────────────────────────
    clause_head("3", "COMPENSATION")
    sub("3.1",
        "Base Salary. The Company shall pay Employee a gross annual base salary of USD "
        "$142,000 (\"Base Salary\"), payable in equal bi-weekly instalments in accordance "
        "with the Company's standard payroll schedule, less required withholdings.")
    sub("3.2",
        "Discretionary Bonus. Employee is eligible for an annual discretionary performance "
        "bonus of up to twenty percent (20%) of Base Salary (\"Target Bonus\"), assessed "
        "against objectives agreed in writing at the start of each calendar year. Payment "
        "of any bonus is at the Company's sole discretion and requires Employee to be "
        "actively employed on the payment date.")
    sub("3.3",
        "Salary Review. Base Salary is reviewed annually, no later than January 31 of each "
        "year. The Company has no obligation to increase Base Salary following any review.")

    # ── 4. BENEFITS ───────────────────────────────────────────────────────────
    clause_head("4", "BENEFITS")
    sub("4.1",
        "Employee shall be entitled to participate in the Company's standard benefit programs, "
        "currently including: (a) medical, dental, and vision insurance (Company pays 80% of "
        "premiums for Employee and eligible dependants); (b) 401(k) plan with Company matching "
        "up to 4% of Base Salary; (c) fifteen (15) days' paid vacation per year, accruing "
        "monthly, non-carrying beyond five (5) days at year-end; and (d) ten (10) Company-"
        "observed public holidays per year.")
    sub("4.2",
        "Benefits are subject to the terms of the applicable plan documents, which the Company "
        "may amend or terminate at any time on reasonable notice. In the event of conflict "
        "between this Agreement and plan documents, the plan documents govern.")

    # ── 5. EXPENSE REIMBURSEMENT ──────────────────────────────────────────────
    clause_head("5", "EXPENSE REIMBURSEMENT")
    sub("5.1",
        "The Company shall reimburse reasonable, pre-approved business expenses upon submission "
        "of receipts and an expense report within thirty (30) days of the expense being "
        "incurred, in accordance with the Company's Travel and Expense Policy.")

    # ── 6. CONFIDENTIALITY AND IP ─────────────────────────────────────────────
    clause_head("6", "CONFIDENTIALITY AND INTELLECTUAL PROPERTY")
    sub("6.1",
        "Employee shall hold all Confidential Information of the Company in strict confidence "
        "and shall not disclose or use it for any purpose other than performing duties "
        "hereunder, both during and for three (3) years after employment ends. \"Confidential "
        "Information\" includes trade secrets, customer data, financial information, product "
        "plans, and any information designated confidential.")
    sub("6.2",
        "All work product, inventions, improvements, and developments created by Employee "
        "within the scope of employment or using Company resources are works made for hire "
        "and are owned exclusively by the Company. Employee irrevocably assigns to the Company "
        "any rights that do not vest automatically as works made for hire.")
    sub("6.3",
        "Employee represents that Schedule B (Prior Inventions) accurately lists all inventions "
        "and developments made prior to employment that Employee wishes to exclude from "
        "Section 6.2. If Schedule B is blank, Employee warrants no such prior inventions exist.")

    # ── 7. NON-COMPETE AND NON-SOLICITATION ───────────────────────────────────
    clause_head("7", "NON-COMPETE AND NON-SOLICITATION")
    sub("7.1",
        "Non-Compete. During employment and for twelve (12) months following termination for "
        "any reason (\"Restricted Period\"), Employee shall not, within a fifty (50) mile "
        "radius of any office where Employee worked in the twelve (12) months prior to "
        "termination, directly or indirectly engage in, own, manage, or provide services to "
        "any business that competes with the Company's enterprise data-management business.")
    sub("7.2",
        "Non-Solicitation. During the Restricted Period, Employee shall not, directly or "
        "indirectly: (a) solicit or attempt to solicit any customer or prospective customer "
        "of the Company with whom Employee had material contact in the twenty-four (24) months "
        "prior to termination; or (b) solicit, recruit, or induce any Company employee to "
        "leave the Company.")
    sub("7.3",
        "Employee acknowledges that the scope, duration, and geographic area of the "
        "restrictions in this Section are reasonable and necessary to protect the Company's "
        "legitimate business interests. If any restriction is held unenforceable, it shall be "
        "modified to the minimum extent necessary to make it enforceable.")

    # ── 8. TERMINATION ────────────────────────────────────────────────────────
    clause_head("8", "TERMINATION")
    sub("8.1",
        "Notice. Either Party may terminate employment without cause by providing the other "
        "Party with four (4) weeks' prior written notice. The Company may, at its election, "
        "pay Employee's Base Salary in lieu of all or part of the notice period.")
    sub("8.2",
        "Summary Dismissal. The Company may terminate employment immediately without notice "
        "or payment in lieu for cause, including but not limited to: (a) gross misconduct or "
        "dishonesty; (b) material breach of this Agreement not cured within five (5) business "
        "days of written notice; (c) conviction of a felony; or (d) wilful violation of "
        "applicable law causing material harm to the Company.")
    sub("8.3",
        "Obligations on Termination. Upon termination, Employee shall: (a) immediately return "
        "all Company property and Confidential Information; (b) resign from all directorships "
        "held on the Company's behalf; and (c) cooperate in transitioning responsibilities "
        "for a period not exceeding four (4) weeks.")

    # ── 9. GENERAL PROVISIONS ─────────────────────────────────────────────────
    clause_head("9", "GENERAL PROVISIONS")
    sub("9.1",
        "This Agreement constitutes the entire agreement between the Parties regarding "
        "Employee's employment and supersedes all prior offers, representations, and "
        "agreements. Amendments require a written instrument signed by both Parties. "
        "This Agreement is governed by the laws of the State of Delaware. Sections 6, 7, "
        "and 9 survive termination. If any provision is held unenforceable, the remainder "
        "continues in full force.")

    # ── SIGNATURE BLOCK ───────────────────────────────────────────────────────
    pdf.ln(2)
    rule()
    col = W / 2 - 4

    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col, LH, "MERIDIAN GROUP LTD")
    pdf.set_x(pdf.l_margin + col + 8)
    pdf.cell(col, LH, "EMPLOYEE", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    for lbl in ["By:", "Name:", "Title:", "Date:"]:
        pdf.ln(4)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_x(pdf.l_margin)
        pdf.cell(col, LH, f"{lbl}  ____________________________")
        pdf.set_x(pdf.l_margin + col + 8)
        pdf.cell(col, LH, f"{lbl}  ____________________________", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(110, 110, 110)
    pdf.multi_cell(W, 4,
                   "Prepared by: Vantage Legal LLP  |  1600 Market Street, Suite 3600, Philadelphia, PA 19103\n"
                   "T: +1 (215) 555-0190  |  legal@vantagelegal.example.com",
                   align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUTPUT))
    size_kb = OUTPUT.stat().st_size / 1024
    print(f"Generated : {OUTPUT.name}")
    print(f"Pages     : {pdf.page}")
    print(f"File size : {size_kb:.1f} KB")


if __name__ == "__main__":
    build()
