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

        # Process every uploaded PDF
        for pdf in uploaded_files:

            saved_path = self.processor.save_uploaded_file(pdf)

            text = self.processor.extract_text(saved_path)

            chunks = self.processor.create_chunks(
                text,
                pdf.name
            )

            # Add chunks from this PDF
            all_chunks.extend(chunks)

        # Create embeddings for all chunks
        texts = [
            chunk["content"]
            for chunk in all_chunks
        ]

        embeddings = self.embedding_manager.embed_documents(texts)

        # Store in ChromaDB
        # self.vector_store.clear_database()   # Uncomment only if you want to reset DB

        self.vector_store.add_chunks(
            all_chunks,
            embeddings
        )

        # Return summary
        return {
            "papers": len(uploaded_files),
            "chunks": len(all_chunks)
        }
