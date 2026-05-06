#!/usr/bin/env python3
"""
Generate docs/nda-template.pdf — 2-page Mutual NDA (Meridian Group Ltd / Apex Dynamics Corp.)

Usage:
    python scripts/gen_nda.py
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos
from pathlib import Path

OUTPUT = Path(__file__).parent.parent / "docs" / "nda-template.pdf"
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
    """Generate the mutual NDA PDF and write it to docs/nda-template.pdf."""
    pdf = LegalPDF(orientation="P", unit="mm", format="LETTER")
    pdf.doc_title = "MUTUAL NON-DISCLOSURE AGREEMENT  |  MERIDIAN GROUP LTD / APEX DYNAMICS CORP."
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
    title_block("MUTUAL NON-DISCLOSURE AGREEMENT")
    subtitle("Effective Date: January 15, 2024")
    rule()

    # ── PARTIES ──────────────────────────────────────────────────────────────
    party_block(
        "MERIDIAN GROUP LTD, a Delaware LLC, 500 Delaware Avenue, Suite 1200, "
        "Wilmington, DE 19801 (\"Meridian\");"
    )
    center_line("and")
    party_block(
        "APEX DYNAMICS CORP., a Delaware corporation, 220 Park Avenue, New York, NY 10169 "
        "(\"Counterparty\"). (Each a \"Party\"; together the \"Parties\".)"
    )
    rule()

    # ── RECITALS ─────────────────────────────────────────────────────────────
    recital(
        "The Parties wish to explore a potential business relationship concerning evaluation "
        "of Meridian's enterprise data-management platform (the \"Purpose\"). In connection "
        "with the Purpose, each Party may disclose non-public and proprietary information to "
        "the other. In consideration of the mutual covenants herein, the Parties agree:"
    )

    # ── 1. DEFINITIONS ────────────────────────────────────────────────────────
    clause_head("1", "DEFINITIONS")
    sub("1.1",
        "\"Confidential Information\" means any information disclosed by one Party "
        "(\"Disclosing Party\") to the other (\"Receiving Party\"), in any form, that is "
        "designated confidential or that a reasonable person would understand to be confidential "
        "given its nature. Confidential Information includes trade secrets, business and "
        "financial plans, customer lists, technical specifications, source code, product "
        "roadmaps, pricing data, and personnel information.")
    sub("1.2",
        "\"Representative\" means employees, officers, directors, counsel, accountants, and "
        "advisors of a Party who need to know Confidential Information solely for the Purpose "
        "and are bound by obligations at least as protective as those herein.")
    sub("1.3",
        "\"Term\" has the meaning set forth in Section 5.1.")

    # ── 2. OBLIGATIONS ────────────────────────────────────────────────────────
    clause_head("2", "OBLIGATIONS OF CONFIDENTIALITY")
    sub("2.1",
        "Each Receiving Party shall: (a) hold Confidential Information in strict confidence; "
        "(b) use it solely for the Purpose; (c) not disclose it to any third party without "
        "prior written consent of the Disclosing Party; and (d) protect it with at least the "
        "same care used for its own most sensitive confidential information, but no less than "
        "reasonable care.")
    sub("2.2",
        "Disclosure to Representatives is permitted only to the extent necessary for the "
        "Purpose. Each Party is liable for breaches by its Representatives.")
    sub("2.3",
        "The Receiving Party shall promptly notify the Disclosing Party of any actual or "
        "suspected unauthorised use or disclosure of Confidential Information.")

    # ── 3. EXCLUSIONS ─────────────────────────────────────────────────────────
    clause_head("3", "EXCLUSIONS FROM CONFIDENTIAL INFORMATION")
    sub("3.1", "Section 2 obligations do not apply to information that the Receiving Party "
        "demonstrates by written evidence:")
    item("a", "is or becomes publicly known through no breach by the Receiving Party;")
    item("b", "was rightfully known before disclosure, evidenced by prior written records;")
    item("c", "is rightfully received from a third party without restriction; or")
    item("d", "is independently developed without reference to the Disclosing Party's information.")

    # ── 4. COMPELLED DISCLOSURE ───────────────────────────────────────────────
    clause_head("4", "COMPELLED DISCLOSURE")
    sub("4.1",
        "If required by law, court order, or governmental authority to disclose Confidential "
        "Information, the Receiving Party shall: (a) give the Disclosing Party at least five "
        "(5) business days' prior written notice (to the extent permitted); (b) cooperate in "
        "seeking a protective order; and (c) disclose only the minimum portion legally required.")

    # ── 5. TERM ───────────────────────────────────────────────────────────────
    clause_head("5", "TERM")
    sub("5.1",
        "This Agreement commences on the Effective Date and continues for two (2) years "
        "(the \"Term\"), unless earlier terminated by either Party on thirty (30) days' "
        "written notice.")
    sub("5.2",
        "Confidentiality obligations under Section 2 survive expiration or termination for "
        "three (3) additional years.")

    # ── 6. RETURN OR DESTRUCTION ──────────────────────────────────────────────
    clause_head("6", "RETURN OR DESTRUCTION OF CONFIDENTIAL INFORMATION")
    sub("6.1",
        "Upon written request or upon expiration or termination, the Receiving Party shall "
        "promptly return or securely destroy all materials embodying Confidential Information "
        "and certify compliance in writing within ten (10) business days. One archival copy "
        "may be retained solely for legal compliance, subject to the obligations herein.")

    # ── 7. REMEDIES ───────────────────────────────────────────────────────────
    clause_head("7", "REMEDIES")
    sub("7.1",
        "Each Party acknowledges that breach of this Agreement may cause irreparable harm "
        "for which monetary damages would be inadequate. The Disclosing Party may seek "
        "injunctive or other equitable relief without bond, in addition to all remedies at "
        "law or equity. The prevailing party in any enforcement action may recover attorneys' "
        "fees and costs.")

    # ── 8. GOVERNING LAW ──────────────────────────────────────────────────────
    clause_head("8", "GOVERNING LAW AND JURISDICTION")
    sub("8.1",
        "This Agreement is governed by the laws of the State of Delaware, without regard to "
        "conflict-of-laws principles. Each Party submits to the exclusive jurisdiction of the "
        "Court of Chancery of the State of Delaware (or, if lacking jurisdiction, the U.S. "
        "District Court for the District of Delaware) for any dispute hereunder.")

    # ── 9. GENERAL PROVISIONS ─────────────────────────────────────────────────
    clause_head("9", "GENERAL PROVISIONS")
    sub("9.1",
        "Entire Agreement. This Agreement is the entire agreement on its subject matter and "
        "supersedes all prior agreements and representations. Amendments require a writing "
        "signed by authorised representatives of both Parties. If any provision is held "
        "unenforceable, it shall be modified to the minimum extent necessary; remaining "
        "provisions remain in effect. No waiver of any right shall arise from failure to "
        "exercise it. This Agreement may be executed in counterparts, including electronically, "
        "each constituting an original.")

    # ── SIGNATURE BLOCK ───────────────────────────────────────────────────────
    pdf.ln(2)
    rule()
    col = W / 2 - 4

    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col, LH, "MERIDIAN GROUP LTD")
    pdf.set_x(pdf.l_margin + col + 8)
    pdf.cell(col, LH, "APEX DYNAMICS CORP.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

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
