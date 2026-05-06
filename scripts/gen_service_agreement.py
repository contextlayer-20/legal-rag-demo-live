#!/usr/bin/env python3
"""
Generate docs/service-agreement.pdf — 3-page Professional Services Agreement
(Meridian Group Ltd / Nexus Consulting Partners LLC)

Usage:
    python scripts/gen_service_agreement.py
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos
from pathlib import Path

OUTPUT = Path(__file__).parent.parent / "docs" / "service-agreement.pdf"
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
    """Generate the professional services agreement PDF and write it to docs/service-agreement.pdf."""
    pdf = LegalPDF(orientation="P", unit="mm", format="LETTER")
    pdf.doc_title = "PROFESSIONAL SERVICES AGREEMENT  |  MERIDIAN GROUP LTD / NEXUS CONSULTING PARTNERS LLC"
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
    title_block("PROFESSIONAL SERVICES AGREEMENT")
    subtitle("Effective Date: February 1, 2024  |  Agreement No. PSA-2024-0042")
    rule()

    # ── PARTIES ──────────────────────────────────────────────────────────────
    party_block(
        "CLIENT: MERIDIAN GROUP LTD, a Delaware limited liability company, 500 Delaware Avenue, "
        "Suite 1200, Wilmington, DE 19801 (\"Client\");"
    )
    center_line("and")
    party_block(
        "SERVICE PROVIDER: NEXUS CONSULTING PARTNERS LLC, a Pennsylvania limited liability "
        "company, 200 South Broad Street, Suite 700, Philadelphia, PA 19102 (\"Provider\"). "
        "(Each a \"Party\"; together the \"Parties\".)"
    )
    rule()

    # ── RECITALS ─────────────────────────────────────────────────────────────
    recital(
        "Client wishes to engage Provider to perform certain professional consulting services, "
        "and Provider wishes to perform such services, on the terms and conditions set forth "
        "herein. In consideration of the mutual covenants and fees described below, the Parties "
        "agree as follows:"
    )

    # ── 1. DEFINITIONS ────────────────────────────────────────────────────────
    clause_head("1", "DEFINITIONS")
    sub("1.1",
        "\"Services\" means the consulting, advisory, and implementation services described in "
        "Schedule A (Statement of Work), as amended by written Change Orders signed by both Parties.")
    sub("1.2",
        "\"Deliverables\" means any work product, reports, analyses, software, or documentation "
        "produced by Provider specifically for Client in performing the Services.")
    sub("1.3",
        "\"Fees\" has the meaning set forth in Section 3.1. \"Background IP\" has the meaning "
        "set forth in Section 4.2.")

    # ── 2. SERVICES AND DELIVERABLES ─────────────────────────────────────────
    clause_head("2", "SERVICES AND DELIVERABLES")
    sub("2.1",
        "Provider shall perform the Services with reasonable care and skill, in accordance with "
        "applicable professional standards, and by the milestones specified in Schedule A. "
        "Provider shall assign qualified personnel and notify Client promptly of any proposed "
        "personnel changes that would materially affect delivery.")
    sub("2.2",
        "Client shall review each Deliverable within ten (10) business days of receipt and "
        "either provide written acceptance or a written list of specific deficiencies. Provider "
        "shall correct identified deficiencies within five (5) business days at no additional "
        "charge. Silence for ten (10) business days constitutes deemed acceptance.")
    sub("2.3",
        "Provider is an independent contractor. Nothing herein creates an employment, "
        "partnership, or joint-venture relationship. Provider is solely responsible for its "
        "personnel's compensation, taxes, insurance, and benefits.")

    # ── 3. FEES AND PAYMENT ───────────────────────────────────────────────────
    clause_head("3", "FEES AND PAYMENT")
    sub("3.1",
        "Client shall pay Provider a monthly retainer of USD $18,500 (the \"Fees\") plus "
        "pre-approved, reasonably documented out-of-pocket expenses. Fees are invoiced on the "
        "first business day of each calendar month.")
    sub("3.2",
        "Payment is due within thirty (30) days of the invoice date (\"Net-30\"). Undisputed "
        "amounts unpaid after thirty (30) days accrue interest at 1.5% per month (or the "
        "maximum permitted by applicable law, if less), compounded monthly.")
    sub("3.3",
        "Client may dispute an invoice in good faith by written notice within ten (10) business "
        "days of receipt, specifying the disputed amount and basis. The Parties shall use "
        "commercially reasonable efforts to resolve the dispute within fifteen (15) business "
        "days. Undisputed portions remain due on the original payment date.")

    # ── 4. INTELLECTUAL PROPERTY ──────────────────────────────────────────────
    clause_head("4", "INTELLECTUAL PROPERTY")
    sub("4.1",
        "All Deliverables are works made for hire to the fullest extent permitted by law. To "
        "the extent any Deliverable does not qualify as a work made for hire, Provider hereby "
        "irrevocably assigns to Client all right, title, and interest therein, including all "
        "copyright, patent, trade-secret, and other intellectual property rights worldwide, "
        "in perpetuity.")
    sub("4.2",
        "Provider retains ownership of its pre-existing tools, methodologies, frameworks, and "
        "general know-how (\"Background IP\"). Provider grants Client a non-exclusive, "
        "royalty-free, perpetual licence to use Background IP incorporated into Deliverables "
        "solely to the extent necessary to use those Deliverables for their intended purpose.")
    sub("4.3",
        "Provider warrants that the Deliverables will not infringe any third-party intellectual "
        "property rights and that Provider has full authority to make the assignments and "
        "grants set out herein.")

    # ── 5. CONFIDENTIALITY ────────────────────────────────────────────────────
    clause_head("5", "CONFIDENTIALITY")
    sub("5.1",
        "Each Party shall hold the other's non-public business, technical, and financial "
        "information (\"Confidential Information\") in strict confidence and use it solely to "
        "perform or receive the Services. Disclosure is permitted only to employees and "
        "contractors with a need to know, bound by equivalent obligations. These obligations "
        "survive expiration or termination for three (3) years.")
    sub("5.2",
        "Confidentiality obligations do not apply to information that: (a) is or becomes "
        "publicly known without breach by the receiving Party; (b) was already known prior "
        "to disclosure; (c) is independently developed without reference to the disclosing "
        "Party's information; or (d) is required to be disclosed by law or court order, "
        "provided the disclosing Party gives prior written notice where legally permissible.")

    # ── 6. LIMITATION OF LIABILITY ────────────────────────────────────────────
    clause_head("6", "LIMITATION OF LIABILITY")
    sub("6.1",
        "TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, NEITHER PARTY SHALL BE LIABLE "
        "FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING "
        "LOSS OF PROFITS, REVENUE, OR DATA, ARISING OUT OF OR RELATED TO THIS AGREEMENT, EVEN "
        "IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.")
    sub("6.2",
        "PROVIDER'S TOTAL CUMULATIVE LIABILITY TO CLIENT SHALL NOT EXCEED THE TOTAL FEES PAID "
        "BY CLIENT IN THE TWELVE (12) CALENDAR MONTHS IMMEDIATELY PRECEDING THE EVENT GIVING "
        "RISE TO THE CLAIM (\"LIABILITY CAP\").")
    sub("6.3",
        "The Liability Cap does not apply to: (a) indemnification obligations under Section 7; "
        "(b) breach of Section 5 (Confidentiality); or (c) liability arising from gross "
        "negligence or wilful misconduct.")

    # ── 7. INDEMNIFICATION ────────────────────────────────────────────────────
    clause_head("7", "INDEMNIFICATION")
    sub("7.1",
        "Provider shall indemnify, defend, and hold harmless Client and its officers, directors, "
        "and employees from third-party claims, losses, and expenses (including reasonable "
        "attorneys' fees) arising from: (a) Provider's material breach of this Agreement; "
        "(b) infringement of third-party IP rights by the Deliverables; or (c) Provider's "
        "gross negligence or wilful misconduct. Client shall promptly notify Provider of any "
        "indemnifiable claim, grant Provider control of the defence, and cooperate reasonably "
        "at Provider's expense.")

    # ── 8. TERM AND TERMINATION ───────────────────────────────────────────────
    clause_head("8", "TERM AND TERMINATION")
    sub("8.1",
        "This Agreement commences on the Effective Date and continues for one (1) year "
        "(the \"Initial Term\"), automatically renewing for successive one-year periods unless "
        "either Party gives sixty (60) days' prior written notice of non-renewal before the "
        "end of the then-current term.")
    sub("8.2",
        "Either Party may terminate this Agreement for convenience on thirty (30) days' prior "
        "written notice. Client shall pay for all Services performed and expenses incurred "
        "through the termination effective date.")
    sub("8.3",
        "Either Party may terminate immediately on written notice if the other Party: "
        "(a) materially breaches and fails to cure within thirty (30) days of written notice; "
        "or (b) becomes insolvent, makes a general assignment for creditors' benefit, or has "
        "a receiver appointed over substantially all its assets.")
    sub("8.4",
        "Sections 4, 5, 6, 7, and 9 survive termination or expiration of this Agreement.")

    # ── 9. GENERAL PROVISIONS ─────────────────────────────────────────────────
    clause_head("9", "GENERAL PROVISIONS")
    sub("9.1",
        "This Agreement, together with all Schedules, constitutes the entire agreement between "
        "the Parties on its subject matter and supersedes all prior agreements. Amendments "
        "require a written instrument signed by authorised representatives of both Parties. "
        "If any provision is held unenforceable, it shall be modified to the minimum extent "
        "necessary; remaining provisions remain in full force. This Agreement is governed by "
        "the laws of the State of Delaware. Each Party submits to the exclusive jurisdiction "
        "of the courts of Delaware for any dispute hereunder.")

    # ── SIGNATURE BLOCK ───────────────────────────────────────────────────────
    pdf.ln(2)
    rule()
    col = W / 2 - 4

    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col, LH, "MERIDIAN GROUP LTD (CLIENT)")
    pdf.set_x(pdf.l_margin + col + 8)
    pdf.cell(col, LH, "NEXUS CONSULTING PARTNERS LLC", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

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
