# Legal Document Q&A — Private RAG Demo by ContextLayer

Ask questions against a set of legal documents and get accurate, cited answers — entirely on your own infrastructure.

![Demo GIF](./assets/demo-testcase.gif)

## One-command setup

```bash
git clone https://github.com/yourusername/legal-rag-demo
cd legal-rag-demo
docker-compose up
# Open http://localhost:8501
```

## What this does

- **Eliminates manual document review** — lawyers and paralegals ask plain-English questions instead of searching PDFs page by page
- **Every answer is verifiable** — source citations link back to the exact document and page, so nothing is taken on faith
- **Fully private** — documents never leave your machine; no third-party API calls, no telemetry

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     docker-compose                       │
│                                                         │
│  ┌──────────────┐   ┌──────────────┐   ┌─────────────┐ │
│  │   Streamlit  │   │    Ollama    │   │   Qdrant    │ │
│  │     app      │──▶│ llama3.1:8b  │   │  vector DB  │ │
│  │  :8501       │   │   :11434     │   │   :6333     │ │
│  └──────┬───────┘   └──────────────┘   └──────┬──────┘ │
│         │                                      │        │
│         └──────────── retrieve ────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

## Stack

| Layer | Tool | Notes |
|---|---|---|
| LLM | Ollama + Llama 3.1 8B | Runs inside Docker, no API key |
| Vector DB | Qdrant | Persistent volume, survives restarts |
| Embeddings | all-MiniLM-L6-v2 | Cached in image at build time |
| RAG Framework | LlamaIndex | Chunking, retrieval, prompt management |
| Frontend | Streamlit | Two-column layout with streaming answers |
| Orchestration | Docker Compose | Three containers, health-checked startup |

## Setup

**Prerequisites:** Docker and Docker Compose installed. 8GB RAM recommended for the LLM.

```bash
# Clone the repo
git clone https://github.com/yourusername/legal-rag-demo
cd legal-rag-demo

# Start the stack (first run pulls ~5GB of model weights)
docker-compose up

# Open the app
open http://localhost:8501
```

On first load, the app automatically ingests the documents in `/docs` into Qdrant. This takes about 30 seconds. After that, the chat interface is ready.

To stop the stack:

```bash
docker-compose down
```

Data persists in Docker volumes (`ollama_data`, `qdrant_data`) between restarts.

## Adding your own documents

1. Drop PDF files into the `/docs` folder
2. Delete the Qdrant volume to force re-ingestion:
   ```bash
   docker-compose down -v
   docker-compose up
   ```
3. The app will re-ingest all documents on the next startup

For large document sets, you can also run ingestion manually:

```bash
docker-compose exec app python scripts/ingest.py
```

## Privacy

This system runs entirely locally. No document content, queries, or answers are sent to any external service. The LLM runs in the Ollama container on your machine. The vector database runs in the Qdrant container on your machine. The only network traffic is between containers on a private Docker network.

---

Built by [ContextLayer](https://contextlayer.io) — private AI infrastructure for professional services firms.
