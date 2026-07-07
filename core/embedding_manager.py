from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL


class EmbeddingManager:
    # Shared model for the entire application
    _model = None

    def __init__(self):
        # Load the model only once
        if EmbeddingManager._model is None:
            print("🔄 Loading embedding model...")
            EmbeddingManager._model = SentenceTransformer(EMBEDDING_MODEL)
            print("✅ Embedding model loaded successfully!")

        self.model = EmbeddingManager._model

    def embed_text(self, text):
        """
        Generate embedding for a single text chunk.
        """
        return self.model.encode(text).tolist()

    def embed_documents(self, texts):
        """
        Generate embeddings for multiple chunks.
        """
        return self.model.encode(texts).tolist()
