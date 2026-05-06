#!/usr/bin/env python3
"""
Load PDF documents from /docs into Qdrant for RAG retrieval.

Usage:
    source .venv/bin/activate
    python scripts/ingest.py

Run once before starting the app. Safe to re-run — skips ingestion if the
collection already has points.
"""

import logging
import sys
from pathlib import Path

# Allow imports from repo root
sys.path.insert(0, str(Path(__file__).parent.parent))

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

import config

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

DOCS_DIR = Path(__file__).parent.parent / "docs"


def get_qdrant_client() -> QdrantClient:
    """Connect to Qdrant and return the client."""
    try:
        client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)
        client.get_collections()
        return client
    except Exception as e:
        log.error("Cannot connect to Qdrant at %s:%s — %s", config.QDRANT_HOST, config.QDRANT_PORT, e)
        log.error("Is Qdrant running? Start it with: docker-compose up qdrant")
        sys.exit(1)


def collection_has_points(client: QdrantClient) -> bool:
    """Return True if the collection exists and contains at least one point."""
    try:
        info = client.get_collection(config.QDRANT_COLLECTION)
        return info.points_count > 0
    except Exception:
        return False


def ensure_collection(client: QdrantClient) -> None:
    """Create the Qdrant collection if it does not exist."""
    existing = [c.name for c in client.get_collections().collections]
    if config.QDRANT_COLLECTION not in existing:
        client.create_collection(
            collection_name=config.QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=config.EMBEDDING_DIMENSIONS,
                distance=Distance.COSINE,
            ),
        )
        log.info("Created collection '%s'", config.QDRANT_COLLECTION)


def load_documents():
    """Load all PDFs from the docs directory."""
    if not DOCS_DIR.exists():
        log.error("Docs directory not found: %s", DOCS_DIR)
        sys.exit(1)

    pdf_files = list(DOCS_DIR.glob("*.pdf"))
    if not pdf_files:
        log.error("No PDF files found in %s", DOCS_DIR)
        sys.exit(1)

    reader = SimpleDirectoryReader(input_dir=str(DOCS_DIR), required_exts=[".pdf"])
    documents = reader.load_data()
    log.info("Loaded %d document pages from %d PDF files", len(documents), len(pdf_files))
    return documents


def ingest() -> None:
    """Run the full ingestion pipeline."""
    client = get_qdrant_client()

    if collection_has_points(client):
        count = client.get_collection(config.QDRANT_COLLECTION).points_count
        log.info("Collection '%s' already has %d points — skipping ingestion", config.QDRANT_COLLECTION, count)
        return

    ensure_collection(client)

    documents = load_documents()

    splitter = SentenceSplitter(chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP)
    nodes = splitter.get_nodes_from_documents(documents)
    log.info("Created %d chunks", len(nodes))

    embed_model = HuggingFaceEmbedding(model_name=config.EMBEDDING_MODEL)
    log.info("Embedding model loaded: %s", config.EMBEDDING_MODEL)

    from qdrant_client.models import PointStruct

    points = []
    for idx, node in enumerate(nodes):
        text = node.get_content()
        vector = embed_model.get_text_embedding(text)

        source_file = Path(node.metadata.get("file_name", "unknown")).name
        page_number = node.metadata.get("page_label", None)
        if page_number is not None:
            try:
                page_number = int(page_number)
            except (ValueError, TypeError):
                page_number = None

        points.append(
            PointStruct(
                id=idx,
                vector=vector,
                payload={
                    "text": text,
                    "source_file": source_file,
                    "page_number": page_number,
                    "chunk_index": idx,
                },
            )
        )

        if (idx + 1) % 10 == 0 or (idx + 1) == len(nodes):
            log.info("Embedded %d / %d chunks", idx + 1, len(nodes))

    client.upsert(collection_name=config.QDRANT_COLLECTION, points=points)
    log.info("Pushed %d points to Qdrant collection '%s'", len(points), config.QDRANT_COLLECTION)


if __name__ == "__main__":
    ingest()
