from core.embedding_manager import EmbeddingManager
from core.vector_store import VectorStore


class Retriever:

    def __init__(self):
        self.embedding_manager = EmbeddingManager()
        self.vector_store = VectorStore()

    def retrieve(self, question, top_k=3, paper_name=None):
        """
        Retrieve the most relevant chunks.
        """

        query_embedding = self.embedding_manager.embed_text(question)

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            paper_name=paper_name
        )

        return results
