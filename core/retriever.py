from core.embedding_manager import EmbeddingManager
from core.vector_store import VectorStore


class Retriever:

    def __init__(self):
        self.embedding_manager = EmbeddingManager()
        self.vector_store = VectorStore()

    def retrieve(self, question, top_k=10):

        query_embedding = self.embedding_manager.embed_text(question)

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        unique_documents = []
        unique_metadata = []

        seen_papers = set()

        for document, metadata in zip(
            results["documents"][0],
            results["metadatas"][0]
        ):

            paper = metadata["paper"]

            if paper not in seen_papers:

                seen_papers.add(paper)

                unique_documents.append(document)

                unique_metadata.append(metadata)

        return {

            "documents": [unique_documents],

            "metadatas": [unique_metadata]

        }
