from core.embedding_manager import EmbeddingManager
from core.vector_store import VectorStore

class Retriever:

    def __init__(self):
        self.embedding_manager = EmbeddingManager()
        self.vector_store = VectorStore()

    def retrieve(
        self,
        question,
        top_k=10,
        paper_name=None
    ):

        query_embedding = self.embedding_manager.embed_text(question)
        print("EMBEDDING:", query_embedding[:5] if query_embedding else query_embedding)

        results = self.vector_store.search(
        query_embedding=query_embedding,
        top_k=top_k,
        paper_name=paper_name
    )

        print("SEARCH RESULT:", results)

        unique_documents = []
        unique_metadata = []

        seen_papers = set()
        DISTANCE_THRESHOLD = 1.2
        for document, metadata,distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]


        ):
            if distance > DISTANCE_THRESHOLD:
                continue

            paper = metadata["paper"]

            if paper not in seen_papers:

                seen_papers.add(paper)

                unique_documents.append(document)

                unique_metadata.append(metadata)

        return {

            "documents": [unique_documents],

            "metadatas": [unique_metadata],

            "found": len(unique_documents) > 0

        }


