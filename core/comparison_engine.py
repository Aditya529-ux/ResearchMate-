from core.vector_store import VectorStore


class ComparisonEngine:

    def __init__(self):
        self.vector_store = VectorStore()

    def compare_papers(self):

        collection = self.vector_store.collection

        data = collection.get()

        metadata = data["metadatas"]

        papers = {}

        for item in metadata:

            paper = item["paper"]

            if paper not in papers:

                papers[paper] = 0

            papers[paper] += 1

        comparison = []

        for paper, chunks in papers.items():

            comparison.append({

                "Paper": paper,

                "Chunks": chunks,

                "Status": "✅ Indexed"

            })

        return comparison
