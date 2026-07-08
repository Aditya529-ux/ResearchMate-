import os
from dotenv import load_dotenv

load_dotenv()

# ==========================
# Google Gemini
# ==========================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GEMINI_MODEL = "gemini-2.5-flash"

# ==========================
# Embedding Model
# ==========================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ==========================
# ChromaDB
# ==========================

VECTOR_DB_PATH = "vectorstore"

# ==========================
# PDF Chunking
# ==========================

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200
