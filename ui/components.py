import streamlit as st


def sidebar():

    with st.sidebar:

        st.header("📂 Documents")

        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=["pdf"],
            accept_multiple_files=True
        )

        process = st.button("Process Documents")

        if process and uploaded_files:

            with st.spinner("Processing PDFs..."):

                from core.pdf_processor import PDFProcessor
                from core.embedding_manager import EmbeddingManager
                from core.vector_store import VectorStore

                processor = PDFProcessor()
                embedding_manager = EmbeddingManager()
                vector_store = VectorStore()

                for pdf in uploaded_files:

                    saved_path = processor.save_uploaded_file(pdf)

                    text = processor.extract_text(saved_path)

                    chunks = processor.create_chunks(
                        text,
                        pdf.name
                    )

                    texts = [chunk["content"] for chunk in chunks]

                    embeddings = embedding_manager.embed_documents(texts)

                    vector_store.add_chunks(chunks, embeddings)

                    st.write(f"{pdf.name} : {len(chunks)} chunks created")

            st.session_state.processed = True
            st.balloons()
            st.success("Processing Complete!")

        st.divider()

        st.subheader("Uploaded Files")

        if uploaded_files:

            for file in uploaded_files:

                st.success(file.name)

        else:

            st.info("No files uploaded.")
