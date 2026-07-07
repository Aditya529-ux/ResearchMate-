from pathlib import Path
import shutil
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class PDFProcessor:
    """
    Handles loading PDF files and extracting text.
    """

    def extract_text(self, pdf_path):
        """
        Extract text from a single PDF.

        Args:
            pdf_path (str or Path): Path to the PDF file.

        Returns:
            str: Extracted text.
        """

        pdf_path = Path(pdf_path)

        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text


    def create_chunks(self, text, paper_name):
        """
        Split extracted text into chunks and attach metadata.
        """

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        texts = splitter.split_text(text)

        chunks = []

        for i, chunk in enumerate(texts):
            chunks.append({
                "content": chunk,
                "metadata": {
                    "paper": paper_name,
                    "chunk_id": i + 1
                }
            })

        return chunks

    def save_uploaded_file(self, uploaded_file):
        """
        Save uploaded Streamlit file into data/uploads.
        """

        upload_path = Path("data/uploads") / uploaded_file.name

        with open(upload_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return upload_path

