class ComparisonEngine:

    def __init__(self):
        pass

    def compare_papers(self, uploaded_files):
        """
        Create a simple comparison table.
        """

        comparison = []

        for file in uploaded_files:

            comparison.append({

                "Paper": file.name,

                "Status": "Indexed"

            })

        return comparison
