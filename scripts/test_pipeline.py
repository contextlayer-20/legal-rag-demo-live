#!/usr/bin/env python3
"""
End-to-end pipeline test: retrieve chunks then stream a generated answer.

Usage:
    source .venv/bin/activate
    QDRANT_HOST=localhost OLLAMA_HOST=localhost python scripts/test_pipeline.py
"""

import os
import sys

# Allow imports from the repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from rag.generator import generate
from rag.retriever import retrieve

TEST_QUESTIONS = [
    "What is the non-compete period in the employment contract?",
    "What are the payment terms in the service agreement?",
    "Who owns the IP for work product created under the IP assignment agreement?",
]


def run_test(question: str) -> None:
    """Retrieve chunks and stream a generated answer for one question."""
    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print("=" * 60)

    chunks = retrieve(question)
    if not chunks:
        print("No chunks retrieved.")
        return

    print(f"Retrieved {len(chunks)} chunks from: {[c['source_file'] for c in chunks]}")
    print("\nAnswer:")

    for token in generate(question, chunks):
        print(token, end="", flush=True)
    print()


if __name__ == "__main__":
    for q in TEST_QUESTIONS:
        run_test(q)
