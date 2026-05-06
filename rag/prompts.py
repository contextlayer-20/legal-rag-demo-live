"""Prompt templates for the legal RAG pipeline."""

from typing import List, Dict, Any


SYSTEM_PROMPT = """You are a legal document assistant. Answer questions using only the document context provided below.

Rules:
- Cite the source filename (e.g. [Source: nda-template.pdf]) for every claim you make.
- If a fact comes from multiple sources, cite each one.
- If the answer is not present in the provided context, respond with exactly: "I cannot find this information in the provided documents."
- Do not infer, speculate, or draw on knowledge outside the provided context.
- Be concise and precise. Use the exact terms and clause numbers from the documents when available."""


def build_user_prompt(context_chunks: List[Dict[str, Any]], question: str) -> str:
    """Build the user-facing prompt from retrieved chunks and the user's question."""
    context_parts = []
    for chunk in context_chunks:
        source = chunk.get("source_file", "unknown")
        text = chunk.get("text", "").strip()
        context_parts.append(f"[Source: {source}]\n{text}")

    context_block = "\n\n".join(context_parts)

    return f"Context:\n{context_block}\n\nQuestion: {question}"
