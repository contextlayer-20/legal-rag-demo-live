#!/usr/bin/env python3
"""Retrieve relevant document chunks from Qdrant for a given query."""

import logging
from typing import Optional

from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from sentence_transformers import SentenceTransformer

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    EMBEDDING_MODEL,
    QDRANT_HOST,
    QDRANT_PORT,
    QDRANT_COLLECTION,
    TOP_K,
)

logger = logging.getLogger(__name__)

_embedding_model: Optional[SentenceTransformer] = None
_qdrant_client: Optional[QdrantClient] = None


def _get_embedding_model() -> SentenceTransformer:
    """Return a cached SentenceTransformer instance."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    return _embedding_model


def _get_qdrant_client() -> QdrantClient:
    """Return a cached QdrantClient instance."""
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    return _qdrant_client


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    """Embed query and return top_k matching chunks from Qdrant with metadata."""
    try:
        model = _get_embedding_model()
        query_vector = model.encode(query).tolist()
    except Exception as exc:
        logger.error("Failed to embed query: %s", exc)
        raise RuntimeError(f"Embedding failed: {exc}") from exc

    try:
        client = _get_qdrant_client()
        response = client.query_points(
            collection_name=QDRANT_COLLECTION,
            query=query_vector,
            limit=top_k,
            with_payload=True,
        )
        results = response.points
    except (UnexpectedResponse, ConnectionError, Exception) as exc:
        logger.error("Qdrant search failed: %s", exc)
        raise RuntimeError(
            f"Could not connect to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}. "
            "Is Qdrant running?"
        ) from exc

    chunks = []
    for hit in results:
        payload = hit.payload or {}
        page_raw = payload.get("page_number")
        chunks.append(
            {
                "text": payload.get("text", ""),
                "source_file": payload.get("source_file", ""),
                "page_number": int(page_raw) if page_raw is not None else None,
                "score": float(hit.score),
            }
        )

    return chunks
