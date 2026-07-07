from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL


class EmbeddingManager:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)

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
