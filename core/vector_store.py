import chromadb
from chromadb.config import Settings


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="vectorstore"
        )

        self.collection = self.client.get_or_create_collection(
            name="researchmate"
        )

    def add_chunks(self, chunks, embeddings):

        ids = []

        documents = []

        metadatas = []

        for i, chunk in enumerate(chunks):

            ids.append(f"chunk_{i}")

            documents.append(chunk["content"])

            metadatas.append(chunk["metadata"])

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )


    def search(self, query_embedding, top_k=3, paper_name=None):

        if paper_name:

            return self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where={"paper": paper_name}
            )

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results

    def clear_database(self):
        """
        Delete all stored chunks from the collection.
        """
        self.client.delete_collection("researchmate")
        self.collection = self.client.get_or_create_collection(
            name="researchmate"
        )
