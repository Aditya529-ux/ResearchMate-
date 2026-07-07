from core.pdf_processor import PDFProcessor
from core.embedding_manager import EmbeddingManager
from core.vector_store import VectorStore



class DocumentService:

    def __init__(self):

        self.processor = PDFProcessor()

        self.embedding_manager = EmbeddingManager()

        self.vector_store = VectorStore()


    def process_documents(self, uploaded_files):
        """
        Process uploaded PDF files and store them in ChromaDB.
        """

        all_chunks = []

        for pdf in uploaded_files:

            saved_path = self.processor.save_uploaded_file(pdf)

            text = self.processor.extract_text(saved_path)

            chunks = self.processor.create_chunks(
                text,
                pdf.name
            )

        all_chunks.extend(chunks)


        texts = [
            chunk["content"]
            for chunk in all_chunks
        ]

        embeddings = self.embedding_manager.embed_documents(
            texts
        )


        self.vector_store.clear_database()

        self.vector_store.add_chunks(
            all_chunks,
            embeddings
        )
        return len(all_chunks)
