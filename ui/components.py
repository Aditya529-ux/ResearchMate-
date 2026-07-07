import streamlit as st

from core.document_service import DocumentService


def sidebar():

    with st.sidebar:

        st.header("📂 Documents")

        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=["pdf"],
            accept_multiple_files=True
        )

        process = st.button("Process Documents")

        if process:

            if not uploaded_files:
                st.warning("Please upload at least one PDF.")
            else:

                with st.spinner("Processing PDFs..."):

                    service = DocumentService()

                    chunk_count = service.process_documents(
                        uploaded_files
                    )

                st.session_state.processed = True

                st.success(
                    f"Successfully processed {chunk_count} chunks!"
                )

                st.balloons()

        st.divider()

        st.subheader("Uploaded Files")

        if uploaded_files:

            for file in uploaded_files:
                st.success(file.name)

        else:
            st.info("No files uploaded.")
