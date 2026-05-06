#!/usr/bin/env python3
"""
Generate docs/privacy-policy.pdf — 2-page Internal Privacy Policy (Meridian Group Ltd).

Covers: data collected, retention periods, third-party sharing, employee rights,
and GDPR compliance statement.

Usage:
    python scripts/gen_privacy_policy.py
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos
from pathlib import Path

OUTPUT = Path(__file__).parent.parent / "docs" / "privacy-policy.pdf"
LH = 4.5
INDENT = 5


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
                  f"Page {self.page_no()} of {{nb}}  |  Prepared by Vantage Legal LLP  |  INTERNAL USE ONLY",
                  align="C")
        self.set_text_color(0, 0, 0)


def build():
    """Generate the Internal Privacy Policy PDF and write it to docs/privacy-policy.pdf."""
    pdf = LegalPDF(orientation="P", unit="mm", format="LETTER")
    pdf.doc_title = "EMPLOYEE DATA PRIVACY POLICY  |  MERIDIAN GROUP LTD  |  v2.1"
    pdf.alias_nb_pages()
    pdf.set_margins(25.4, 22, 25.4)
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    W = pdf.epw

    def title_block(text):
        pdf.set_font("Helvetica", "B", 15)
        pdf.multi_cell(W, 8, text, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1)

    def subtitle(text):
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(W, 4.5, text, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

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

    def item(bullet, text):
        pdf.set_x(pdf.l_margin + INDENT * 2)
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(W - INDENT * 2, LH, f"{bullet}  {text}", align="J",
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(0.3)

    def table_row(label, value, shaded=False):
        if shaded:
            pdf.set_fill_color(245, 245, 245)
        else:
            pdf.set_fill_color(255, 255, 255)
        col1 = W * 0.38
        col2 = W * 0.62
        pdf.set_font("Helvetica", "B", 8.5)
        y = pdf.get_y()
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(col1, LH, label, border=1, fill=True, align="L",
                       new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_y(y)
        pdf.set_x(pdf.l_margin + col1)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.multi_cell(col2, LH, value, border=1, fill=True, align="L",
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ── TITLE ────────────────────────────────────────────────────────────────
    pdf.ln(2)
    title_block("EMPLOYEE DATA PRIVACY POLICY")
    subtitle(
        "Meridian Group Ltd  |  Policy Reference: HR-PRIV-2024-02  |  Version 2.1\n"
        "Effective Date: April 1, 2024  |  Review Date: April 1, 2025"
    )
    rule()

    # ── SCOPE & PURPOSE ───────────────────────────────────────────────────────
    clause_head("1", "SCOPE AND PURPOSE")
    sub("1.1",
        "This policy applies to all employees, contractors, secondees, and interns of "
        "Meridian Group Ltd (\"Meridian\" or \"Company\") whose personal data is processed "
        "by the Company in connection with their employment or engagement. It describes "
        "how Meridian collects, uses, stores, and shares personal data and sets out the "
        "rights of data subjects under applicable data protection law, including the "
        "General Data Protection Regulation (EU) 2016/679 (\"GDPR\") and the UK GDPR.")
    sub("1.2",
        "This policy does not form part of any employee's contract of employment and "
        "may be updated from time to time. The Data Protection Officer (\"DPO\") is "
        "responsible for maintaining this policy. Questions should be directed to "
        "dpo@meridiangroup.example.com.")

    # ── DATA COLLECTED ────────────────────────────────────────────────────────
    clause_head("2", "CATEGORIES OF PERSONAL DATA COLLECTED")
    sub("2.1",
        "Meridian collects and processes the following categories of personal data "
        "about employees and contractors:")
    item("(a)", "Identity data: full legal name, date of birth, national insurance or "
         "social security number, passport or government-issued ID number.")
    item("(b)", "Contact data: home address, personal telephone number, personal email "
         "address, and emergency contact details.")
    item("(c)", "Employment data: job title, department, employment start and end dates, "
         "remuneration, bonus and equity records, performance reviews, disciplinary "
         "records, and training records.")
    item("(d)", "Financial data: bank account details for payroll, tax withholding "
         "records, expense claims, and benefit elections.")
    item("(e)", "Health and wellbeing data (special category): medical certificates, "
         "occupational health reports, and disability accommodation requests, processed "
         "only where strictly necessary and with appropriate safeguards.")
    item("(f)", "Technical data: corporate device identifiers, system access logs, "
         "email metadata, and VPN connection records generated in the ordinary course "
         "of IT systems management.")
    sub("2.2",
        "Meridian relies on the following legal bases to process personal data: "
        "(i) performance of the employment contract (Article 6(1)(b) GDPR); "
        "(ii) compliance with legal obligations, including tax and employment law "
        "(Article 6(1)(c)); (iii) legitimate interests in managing its workforce and "
        "securing its systems (Article 6(1)(f)); and (iv) explicit consent where required "
        "for special-category data (Article 9(2)(a)).")

    # ── RETENTION PERIODS ─────────────────────────────────────────────────────
    clause_head("3", "DATA RETENTION PERIODS")
    sub("3.1",
        "Meridian retains personal data only for as long as necessary for the purposes "
        "for which it was collected, subject to the minimum retention periods set out "
        "in the table below. Where data is retained beyond the periods below, a written "
        "justification approved by the DPO is required.")
    pdf.ln(1)
    table_row("Data Category", "Retention Period", shaded=False)
    table_row("Employment records (active)", "Duration of employment + 7 years", shaded=True)
    table_row("Payroll and tax records", "7 years from end of tax year", shaded=False)
    table_row("Recruitment records (unsuccessful)", "12 months from decision date", shaded=True)
    table_row("Disciplinary and grievance records", "5 years from resolution", shaded=False)
    table_row("Health and occupational health data", "Duration of employment + 3 years", shaded=True)
    table_row("IT access and security logs", "12 months on a rolling basis", shaded=False)
    table_row("CCTV footage (where applicable)", "31 days unless flagged for investigation", shaded=True)
    pdf.ln(2)
    sub("3.2",
        "At the end of the applicable retention period, personal data shall be securely "
        "deleted or anonymised in accordance with Meridian's Data Disposal Standard "
        "(HR-SEC-2024-01). The DPO reviews retention schedules annually.")

    # ── THIRD-PARTY SHARING ───────────────────────────────────────────────────
    clause_head("4", "THIRD-PARTY SHARING")
    sub("4.1",
        "Meridian does not sell personal data. Personal data may be shared with "
        "third parties only in the following circumstances:")
    item("(a)", "Payroll and benefits providers: ADP Workforce Now (payroll processor) "
         "and Willis Towers Watson (benefits administrator) receive identity, employment, "
         "and financial data under data processing agreements that comply with Article 28 "
         "GDPR.")
    item("(b)", "Legal and regulatory authorities: personal data may be disclosed to "
         "HMRC, the IRS, the SEC, or other regulators where required by law or court "
         "order. Meridian will notify the affected individual unless prohibited from doing so.")
    item("(c)", "Professional advisers: Vantage Legal LLP (legal counsel) and Grant "
         "Thornton LLP (external auditors) may receive personal data under strict "
         "confidentiality obligations.")
    item("(d)", "Group companies: personal data may be transferred to affiliated entities "
         "within the Meridian Group for HR administration purposes, subject to intra-group "
         "data transfer agreements.")
    sub("4.2",
        "Where personal data is transferred outside the European Economic Area or the "
        "United Kingdom, Meridian ensures an adequate level of protection through "
        "Standard Contractual Clauses approved by the European Commission "
        "(Decision 2021/914) or the UK International Data Transfer Agreement, as applicable.")

    # ── EMPLOYEE RIGHTS ───────────────────────────────────────────────────────
    clause_head("5", "EMPLOYEE RIGHTS UNDER DATA PROTECTION LAW")
    sub("5.1",
        "Employees and contractors have the following rights with respect to their "
        "personal data held by Meridian:")
    item("(a)", "Right of access (Article 15 GDPR): to request a copy of personal data "
         "held, within 30 days of a verified subject access request.")
    item("(b)", "Right to rectification (Article 16): to request correction of inaccurate "
         "or incomplete personal data without undue delay.")
    item("(c)", "Right to erasure (Article 17): to request deletion where data is no "
         "longer necessary, consent is withdrawn, or processing is unlawful, subject to "
         "overriding legal obligations.")
    item("(d)", "Right to restriction (Article 18): to request that processing be "
         "restricted while accuracy or lawfulness is contested.")
    item("(e)", "Right to data portability (Article 20): to receive personal data provided "
         "on the basis of consent or contract in a structured, machine-readable format.")
    item("(f)", "Right to object (Article 21): to object to processing based on legitimate "
         "interests, including profiling.")
    sub("5.2",
        "Requests to exercise any of the above rights should be submitted in writing "
        "to dpo@meridiangroup.example.com. Meridian will respond within 30 calendar days. "
        "Where a request is complex or numerous, Meridian may extend this period by up to "
        "two additional months with written notice.")
    sub("5.3",
        "Employees have the right to lodge a complaint with the relevant supervisory "
        "authority. For UK employees, this is the Information Commissioner's Office (ICO) "
        "at ico.org.uk. For EU employees, this is the supervisory authority in the member "
        "state of habitual residence or place of work.")

    # ── GDPR COMPLIANCE ───────────────────────────────────────────────────────
    clause_head("6", "GDPR COMPLIANCE STATEMENT")
    sub("6.1",
        "Meridian Group Ltd is committed to full compliance with the GDPR and all "
        "applicable national data protection legislation. Meridian has appointed a "
        "Data Protection Officer, maintains a Record of Processing Activities ("
        "\"ROPA\") as required by Article 30 GDPR, and conducts Data Protection Impact "
        "Assessments (\"DPIAs\") for high-risk processing activities.")
    sub("6.2",
        "Meridian implements appropriate technical and organisational measures to ensure "
        "a level of security appropriate to the risk, including: (a) encryption of "
        "personal data at rest and in transit using AES-256 and TLS 1.3; (b) role-based "
        "access controls limiting data access to authorised personnel; (c) regular "
        "penetration testing and vulnerability assessments; and (d) mandatory annual "
        "data protection training for all staff.")
    sub("6.3",
        "In the event of a personal data breach, Meridian will notify the relevant "
        "supervisory authority within 72 hours of becoming aware of the breach, where "
        "feasible, in accordance with Article 33 GDPR. Where the breach is likely to "
        "result in a high risk to affected individuals, Meridian will also notify those "
        "individuals without undue delay under Article 34 GDPR.")
    sub("6.4",
        "This policy is reviewed annually by the DPO and approved by the Board of "
        "Directors. The most recent review was completed on March 15, 2024. Material "
        "changes to this policy will be communicated to all employees within 14 days "
        "of approval.")

    # ── CONTACT ───────────────────────────────────────────────────────────────
    clause_head("7", "CONTACT AND ESCALATION")
    sub("7.1",
        "Data Protection Officer: Sarah K. Whitmore, Meridian Group Ltd, "
        "500 Delaware Avenue, Suite 1200, Wilmington, DE 19801. "
        "Email: dpo@meridiangroup.example.com. Tel: +1 (302) 555-0147.")
    sub("7.2",
        "External legal counsel on data protection matters: Vantage Legal LLP, "
        "1600 Market Street, Suite 3600, Philadelphia, PA 19103. "
        "Contact: privacy@vantagelegal.example.com.")

    # ── FOOTER BLOCK ─────────────────────────────────────────────────────────
    pdf.ln(2)
    rule()
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(110, 110, 110)
    pdf.multi_cell(
        W, 4,
        "Approved by: Board of Directors, Meridian Group Ltd  |  Approval Date: March 22, 2024\n"
        "Prepared by: Vantage Legal LLP  |  1600 Market Street, Suite 3600, Philadelphia, PA 19103\n"
        "Policy Reference: HR-PRIV-2024-02  |  Next Review: April 1, 2025",
        align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT
    )
    pdf.set_text_color(0, 0, 0)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUTPUT))
    size_kb = OUTPUT.stat().st_size / 1024
    print(f"Generated : {OUTPUT.name}")
    print(f"Pages     : {pdf.page}")
    print(f"File size : {size_kb:.1f} KB")


if __name__ == "__main__":
    build()
