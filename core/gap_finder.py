from core.vector_store import VectorStore


class GapFinder:

    def __init__(self):
        self.vector_store = VectorStore()

    def analyze(self):

        collection = self.vector_store.collection

        data = collection.get()

        metadata = data["metadatas"]

        papers = {}

        for item in metadata:

            paper = item["paper"]

            papers[paper] = papers.get(paper, 0) + 1

        report = {

            "papers": len(papers),

            "chunks": len(metadata),

            "status": "Ready for AI Analysis"

        }

        if len(papers) < 2:

            report["message"] = (
                "Upload at least two research papers "
                "for meaningful comparison."
            )

        else:

            report["message"] = (
                "Enough papers uploaded. "
                "Research gap analysis can be performed."
            )

        return report
