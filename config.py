import os
from dotenv import load_dotenv

load_dotenv()

# Qdrant
QDRANT_URL = os.environ.get("QDRANT_URL", "")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY", "")
QDRANT_COLLECTION = "legal-docs"

# Groq
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.1-8b-instant"

# Embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSIONS = 384

# Chunking
CHUNK_SIZE = 512
CHUNK_OVERLAP = 64

# Retrieval
TOP_K = 5

# Demo limits
MAX_QUERIES_PER_SESSION = 0     # 0 = no limit (local/GitHub demo)
                                # Set to 10 for hosted/public demo

# Branding
DEMO_NAME = "Legal Document Q&A"
DEMO_VERTICAL = "Legal"
ACCENT_COLOR = "#4f8ef7"
