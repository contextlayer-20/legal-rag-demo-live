"""Streamlit frontend for the ContextLayer Legal RAG Demo."""

import logging
import subprocess
import sys
from pathlib import Path

import streamlit as st
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse

from config import (
    ACCENT_COLOR,
    DEMO_NAME,
    MAX_QUERIES_PER_SESSION,
    QDRANT_COLLECTION,
    QDRANT_HOST,
    QDRANT_PORT,
)
from rag.generator import generate
from rag.retriever import retrieve

logger = logging.getLogger(__name__)

DOCS_DIR = Path(__file__).parent / "docs"
INGEST_SCRIPT = Path(__file__).parent / "scripts" / "ingest.py"

_DOC_DESCRIPTIONS: dict[str, str] = {
    "nda-template.pdf": "Mutual NDA — confidentiality, obligations, 2-year term",
    "service-agreement.pdf": "Services, payment terms (net-30), IP ownership",
    "employment-contract.pdf": "Role, compensation, non-compete, termination",
    "ip-assignment.pdf": "Work product assignment, moral rights waiver",
    "privacy-policy.pdf": "Data retention, third-party sharing, GDPR",
}


def _collection_has_points() -> bool:
    """Return True if the Qdrant collection exists and contains at least one point."""
    try:
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        info = client.get_collection(QDRANT_COLLECTION)
        return (info.points_count or 0) > 0
    except (UnexpectedResponse, Exception):
        return False


def _run_ingestion() -> None:
    """Invoke the ingest script as a subprocess and stop on failure."""
    result = subprocess.run(
        [sys.executable, str(INGEST_SCRIPT)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        st.error(f"Knowledge base ingestion failed:\n{result.stderr}")
        st.stop()


def _apply_styles() -> None:
    """Inject custom dark-theme CSS with DM Mono font."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,400;0,500;1,400&display=swap');

        html, body, [class*="css"] {{
            font-family: 'DM Mono', monospace !important;
            background-color: #0d1117;
            color: #c9d1d9;
        }}
        .stApp {{
            background-color: #0d1117;
        }}
        [data-testid="stChatMessage"] {{
            background-color: #0f1923;
            border: 1px solid #1a2535;
            border-radius: 6px;
            padding: 0.75rem;
        }}
        [data-testid="stChatInputContainer"] {{
            border-top: 1px solid #1a2535;
        }}
        [data-testid="stExpander"] {{
            background-color: #0f1923;
            border: 1px solid #1a2535 !important;
        }}
        a {{
            color: {ACCENT_COLOR} !important;
        }}
        .stButton > button, .stDownloadButton > button {{
            background-color: #1a2535;
            color: #c9d1d9;
            border: 1px solid {ACCENT_COLOR};
            font-family: 'DM Mono', monospace;
            border-radius: 4px;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{
            background-color: {ACCENT_COLOR};
            color: #0d1117;
        }}
        hr {{
            border-color: #1a2535;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _init_session_state() -> None:
    """Initialise all session state keys on first load."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "query_count" not in st.session_state:
        st.session_state.query_count = 0
    if "ingestion_complete" not in st.session_state:
        st.session_state.ingestion_complete = False


def _citations_panel(chunks: list[dict], idx: int | str) -> None:
    """Render a collapsible citations panel for the given retrieved chunks."""
    seen: dict[str, dict] = {}
    for chunk in chunks:
        src = chunk["source_file"]
        if src not in seen:
            seen[src] = chunk

    label = f"Sources ({len(seen)} document{'s' if len(seen) != 1 else ''})"
    with st.expander(label):
        for src, chunk in seen.items():
            st.markdown(f"**{src}**")
            excerpt = chunk["text"][:200].strip()
            if len(chunk["text"]) > 200:
                excerpt += "…"
            st.caption(excerpt)
            if chunk["page_number"] is not None:
                st.caption(f"Page {chunk['page_number']}")
            pdf_path = DOCS_DIR / src
            if pdf_path.exists():
                with open(pdf_path, "rb") as fh:
                    st.download_button(
                        label=f"Download {src}",
                        data=fh.read(),
                        file_name=src,
                        mime="application/pdf",
                        key=f"cite_{idx}_{src}",
                    )
            st.divider()


def _render_history() -> None:
    """Render all messages stored in session state."""
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("chunks"):
                _citations_panel(msg["chunks"], idx=i)


def _render_document_library() -> None:
    """Render the document library section in the right column."""
    st.markdown("#### KNOWLEDGE BASE")
    pdfs = sorted(DOCS_DIR.glob("*.pdf"))
    for pdf in pdfs:
        name = pdf.stem.replace("-", " ").title()
        desc = _DOC_DESCRIPTIONS.get(pdf.name, "")
        st.markdown(f"**{name}**")
        if desc:
            st.caption(desc)
        with open(pdf, "rb") as fh:
            st.download_button(
                label="Download",
                data=fh.read(),
                file_name=pdf.name,
                mime="application/pdf",
                key=f"lib_{pdf.name}",
            )

    st.divider()
    st.markdown("#### SESSION")

    if MAX_QUERIES_PER_SESSION > 0:
        remaining = max(0, MAX_QUERIES_PER_SESSION - st.session_state.query_count)
        st.markdown(f"**{remaining} of {MAX_QUERIES_PER_SESSION} queries remaining**")
        st.progress(remaining / MAX_QUERIES_PER_SESSION)
    else:
        st.markdown("**Unlimited queries**")


def main() -> None:
    """Entry point — configure page, check ingestion, render layout."""
    st.set_page_config(
        page_title=f"ContextLayer — {DEMO_NAME}",
        page_icon="⚖️",
        layout="wide",
    )
    _apply_styles()
    _init_session_state()

    st.markdown(f"## ContextLayer  /  {DEMO_NAME}")
    st.caption(
        "*Ask questions against the knowledge base. "
        "Every answer includes a source citation you can verify.*"
    )

    if not st.session_state.ingestion_complete:
        if not _collection_has_points():
            with st.spinner("Loading knowledge base…"):
                _run_ingestion()
        st.session_state.ingestion_complete = True

    col_chat, col_docs = st.columns([2, 1])

    with col_docs:
        _render_document_library()

    with col_chat:
        _render_history()

        limit_reached = (
            MAX_QUERIES_PER_SESSION > 0
            and st.session_state.query_count >= MAX_QUERIES_PER_SESSION
        )

        if limit_reached:
            st.warning(
                "Demo query limit reached. "
                "Contact ContextLayer to discuss your use case."
            )
        else:
            question = st.chat_input("Ask a question about the legal documents…")

            if question:
                st.session_state.messages.append(
                    {"role": "user", "content": question}
                )
                with st.chat_message("user"):
                    st.markdown(question)

                chunks = retrieve(question)
                new_idx = len(st.session_state.messages)

                with st.chat_message("assistant"):
                    answer: str = st.write_stream(generate(question, chunks))
                    _citations_panel(chunks, idx=new_idx)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "chunks": chunks}
                )
                st.session_state.query_count += 1


if __name__ == "__main__":
    main()
