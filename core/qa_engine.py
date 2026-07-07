import google.generativeai as genai

from config import GEMINI_API_KEY, GEMINI_MODEL


class QAEngine:

    def __init__(self):

        genai.configure(api_key=GEMINI_API_KEY)

        self.model = genai.GenerativeModel(
            GEMINI_MODEL
        )

    def answer_question(self, question, documents, metadatas):

        context = ""

        sources = []

        for doc, meta in zip(documents, metadatas):

            context += f"\nPaper: {meta['paper']}\n"

            context += doc + "\n\n"

            sources.append(meta["paper"])

        prompt = f"""
You are ResearchMate.

Answer ONLY using the information below.

If the answer is not present, say:

"I couldn't find the answer in the uploaded papers."

Context:

{context}

Question:

{question}

Give a concise answer.

At the end write:

Sources:
"""

        response = self.model.generate_content(prompt)

        return {

            "answer": response.text,

            "sources": list(set(sources))

        }
