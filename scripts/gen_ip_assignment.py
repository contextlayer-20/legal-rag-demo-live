#!/usr/bin/env python3
"""
Generate docs/ip-assignment.pdf — 2-page IP Assignment Agreement (Meridian Group Ltd).

Covers: assignment of work product, moral rights waiver, prior inventions
carve-out, and consideration.

Usage:
    python scripts/gen_ip_assignment.py
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos
from pathlib import Path

OUTPUT = Path(__file__).parent.parent / "docs" / "ip-assignment.pdf"
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
                  f"Page {self.page_no()} of {{nb}}  |  Prepared by Vantage Legal LLP  |  CONFIDENTIAL",
                  align="C")
        self.set_text_color(0, 0, 0)


def build():
    """Generate the IP Assignment Agreement PDF and write it to docs/ip-assignment.pdf."""
    pdf = LegalPDF(orientation="P", unit="mm", format="LETTER")
    pdf.doc_title = "INTELLECTUAL PROPERTY ASSIGNMENT AGREEMENT  |  MERIDIAN GROUP LTD"
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
    title_block("INTELLECTUAL PROPERTY ASSIGNMENT AGREEMENT")
    subtitle("Effective Date: March 1, 2024")
    rule()

    # ── PARTIES ──────────────────────────────────────────────────────────────
    party_block(
        "MERIDIAN GROUP LTD, a Delaware limited liability company, 500 Delaware Avenue, "
        "Suite 1200, Wilmington, DE 19801 (\"Company\");"
    )
    center_line("and")
    party_block(
        "JULIAN R. HARTLEY, an individual, residing at 44 Birchwood Drive, Wilmington, "
        "DE 19802 (\"Assignor\"). (Each a \"Party\"; together the \"Parties\".)"
    )
    rule()

    # ── RECITALS ─────────────────────────────────────────────────────────────
    recital(
        "Company has engaged Assignor as an independent contractor under a separate "
        "Statement of Work dated February 12, 2024 (the \"SOW\") to develop certain "
        "software, systems, and related materials. In consideration of the fees paid "
        "under the SOW and the mutual covenants herein, the Parties agree as follows:"
    )

    # ── 1. DEFINITIONS ────────────────────────────────────────────────────────
    clause_head("1", "DEFINITIONS")
    sub("1.1",
        "\"Work Product\" means all inventions, discoveries, improvements, works of "
        "authorship, software (including source code, object code, and documentation), "
        "algorithms, databases, know-how, techniques, and other materials conceived, "
        "created, or first reduced to practice by Assignor, alone or jointly with others, "
        "in connection with the SOW or using Company resources, whether or not patentable "
        "or copyrightable.")
    sub("1.2",
        "\"Prior Inventions\" means all inventions, works, and materials made by Assignor "
        "prior to the Effective Date that are listed in Exhibit A attached hereto. "
        "Assignor represents that Exhibit A is a complete and accurate list of all Prior "
        "Inventions that Assignor wishes to exclude from the assignment under Section 2.")
    sub("1.3",
        "\"Moral Rights\" means any rights of attribution, integrity, disclosure, "
        "withdrawal, or other author's rights recognised under applicable law.")

    # ── 2. ASSIGNMENT OF WORK PRODUCT ─────────────────────────────────────────
    clause_head("2", "ASSIGNMENT OF WORK PRODUCT")
    sub("2.1",
        "Assignor hereby irrevocably assigns to Company, for the full term of all "
        "intellectual property rights and any extensions or renewals thereof, all right, "
        "title, and interest in and to all Work Product, including all patent rights, "
        "copyrights, trade secret rights, trademark rights, and any other proprietary "
        "rights worldwide. This assignment is effective as of the moment each item of "
        "Work Product is created.")
    sub("2.2",
        "If any Work Product cannot be assigned under applicable law, Assignor grants "
        "Company an exclusive, worldwide, royalty-free, irrevocable, perpetual licence "
        "with the right to sublicence, to use, reproduce, distribute, prepare derivative "
        "works of, display, and perform such Work Product in any medium now known or "
        "hereafter developed.")
    sub("2.3",
        "Assignor shall, at Company's request and expense, execute all documents and "
        "take all actions reasonably necessary to perfect, record, or enforce Company's "
        "rights in Work Product, including executing patent applications and assignments "
        "in any jurisdiction.")

    # ── 3. MORAL RIGHTS WAIVER ────────────────────────────────────────────────
    clause_head("3", "MORAL RIGHTS WAIVER")
    sub("3.1",
        "To the fullest extent permitted by applicable law, Assignor irrevocably waives "
        "and agrees never to assert any Moral Rights in or relating to any Work Product "
        "against Company or its licensees, successors, or assigns. Where such waiver is "
        "not permitted by law, Assignor unconditionally consents to any action by Company "
        "that would otherwise infringe such Moral Rights.")
    sub("3.2",
        "Assignor acknowledges that Company shall have the right to modify, adapt, "
        "translate, create derivative works of, and use Work Product without attribution "
        "to Assignor in any form or context, including commercial use.")

    # ── 4. PRIOR INVENTIONS CARVE-OUT ─────────────────────────────────────────
    clause_head("4", "PRIOR INVENTIONS CARVE-OUT")
    sub("4.1",
        "The assignment in Section 2 expressly excludes any Prior Inventions listed in "
        "Exhibit A. Assignor grants Company a non-exclusive, royalty-free, worldwide "
        "licence to any Prior Invention that is incorporated into or necessary for the "
        "use of Work Product.")
    sub("4.2",
        "If Assignor fails to list any invention on Exhibit A, Assignor represents and "
        "warrants that no such unlisted invention is incorporated into Work Product. "
        "If an unlisted invention is later found to be incorporated, it shall be deemed "
        "Work Product subject to full assignment under Section 2.")
    sub("4.3",
        "Assignor warrants that the Prior Inventions listed in Exhibit A do not infringe "
        "any third-party intellectual property rights and that Assignor has the full "
        "authority to grant the licence described in Section 4.1.")

    # ── 5. CONSIDERATION ──────────────────────────────────────────────────────
    clause_head("5", "CONSIDERATION")
    sub("5.1",
        "In consideration for the assignment and waivers herein, Company shall pay "
        "Assignor the fees set forth in the SOW, which constitute fair and adequate "
        "consideration for all rights transferred. Assignor acknowledges receipt of "
        "consideration and agrees that no further compensation is owed for the "
        "intellectual property rights assigned hereunder.")
    sub("5.2",
        "Company's obligation to pay fees under the SOW is independent of and shall not "
        "be affected by any dispute regarding ownership of Work Product. Assignor shall "
        "not withhold performance of obligations under this Agreement pending resolution "
        "of any payment dispute.")

    # ── 6. REPRESENTATIONS AND WARRANTIES ────────────────────────────────────
    clause_head("6", "REPRESENTATIONS AND WARRANTIES")
    sub("6.1", "Assignor represents and warrants that:")
    item("a", "Assignor has the full right and authority to enter into this Agreement and "
         "to assign the rights described herein;")
    item("b", "the Work Product will be original and will not infringe any third-party "
         "intellectual property right, privacy right, or other proprietary right;")
    item("c", "no portion of the Work Product is subject to any lien, encumbrance, or "
         "third-party claim; and")
    item("d", "Assignor has not granted and will not grant any third party any right or "
         "licence that would conflict with the assignment herein.")

    # ── 7. CONFIDENTIALITY ────────────────────────────────────────────────────
    clause_head("7", "CONFIDENTIALITY")
    sub("7.1",
        "Assignor acknowledges that Work Product and all information relating thereto "
        "constitutes confidential information of Company. Assignor shall not, during or "
        "after the term of the SOW, disclose any Work Product or related information to "
        "any third party without Company's prior written consent, except as required by "
        "law.")

    # ── 8. GOVERNING LAW ──────────────────────────────────────────────────────
    clause_head("8", "GOVERNING LAW AND DISPUTE RESOLUTION")
    sub("8.1",
        "This Agreement is governed by the laws of the State of Delaware, without regard "
        "to conflict-of-laws principles. Any dispute arising hereunder shall be submitted "
        "to binding arbitration administered by JAMS in Wilmington, Delaware, under its "
        "Streamlined Arbitration Rules, except that either Party may seek injunctive "
        "relief in any court of competent jurisdiction to prevent irreparable harm.")

    # ── 9. GENERAL PROVISIONS ─────────────────────────────────────────────────
    clause_head("9", "GENERAL PROVISIONS")
    sub("9.1",
        "This Agreement constitutes the entire agreement between the Parties relating to "
        "its subject matter and supersedes all prior negotiations and representations. "
        "Amendments require a signed writing. If any provision is unenforceable, it shall "
        "be modified to the minimum extent necessary; remaining provisions continue in "
        "full force. This Agreement binds and inures to the benefit of the Parties and "
        "their respective heirs, successors, and assigns. Company may assign this "
        "Agreement without Assignor's consent.")

    # ── EXHIBIT A PLACEHOLDER ─────────────────────────────────────────────────
    pdf.ln(2)
    rule()
    pdf.set_font("Helvetica", "B", 10)
    pdf.multi_cell(W, LH, "EXHIBIT A - PRIOR INVENTIONS", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(
        W, LH,
        "The following is a complete list of Prior Inventions that Assignor excludes from "
        "the assignment under Section 2 of the Agreement (check one):",
        align="J", new_x=XPos.LMARGIN, new_y=YPos.NEXT
    )
    pdf.ln(2)
    pdf.multi_cell(W, LH, "[ ]  No Prior Inventions.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)
    pdf.multi_cell(
        W, LH,
        "[ ]  See list below:\n\n"
        "___________________________________________________________________________\n\n"
        "___________________________________________________________________________\n\n"
        "___________________________________________________________________________",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT
    )

    # ── SIGNATURE BLOCK ───────────────────────────────────────────────────────
    pdf.ln(4)
    rule()
    col = W / 2 - 4

    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col, LH, "MERIDIAN GROUP LTD (\"Company\")")
    pdf.set_x(pdf.l_margin + col + 8)
    pdf.cell(col, LH, "ASSIGNOR", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

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
    pdf.multi_cell(
        W, 4,
        "Prepared by: Vantage Legal LLP  |  1600 Market Street, Suite 3600, Philadelphia, PA 19103\n"
        "T: +1 (215) 555-0190  |  legal@vantagelegal.example.com",
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
