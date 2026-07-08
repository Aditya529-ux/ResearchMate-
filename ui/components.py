import streamlit as st

from core.document_service import DocumentService
from core.vector_store import VectorStore


def sidebar():

    with st.sidebar:

        st.header("📂 Documents")

        # ---------------- Upload ---------------- #

        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=["pdf"],
            accept_multiple_files=True
        )

        if uploaded_files:
            st.session_state.uploaded_files = uploaded_files

        # ---------------- Process ---------------- #

        if st.button("Process Documents"):

            if not uploaded_files:

                st.warning("Please upload at least one PDF.")

            else:

                with st.spinner("Processing PDFs..."):

                    service = DocumentService()

                    summary = service.process_documents(
                        uploaded_files
                    )

                # Save everything in Session State
                st.session_state.summary = summary
                st.session_state.processed = True

                st.success("✅ Documents processed successfully!")

        # ---------------- Knowledge Base ---------------- #

        st.divider()

        st.subheader("📚 Knowledge Base")

        summary = st.session_state.get("summary")

        if summary:

            st.success("🟢 Ready")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Papers",
                    summary.get("papers", 0)
                )

            with col2:
                st.metric(
                    "Chunks",
                    summary.get("chunks", 0)
                )

        else:

            st.info("No documents processed yet.")

        # ---------------- Uploaded Papers ---------------- #

        st.divider()

        st.subheader("📄 Uploaded Papers")

        files = st.session_state.get("uploaded_files", [])

        if files:

            for file in files:

                st.write(f"✅ {file.name}")

        else:

            st.caption("No papers uploaded.")

        # ---------------- Reset ---------------- #

        st.divider()

        if st.button("🗑 Reset Knowledge Base"):

            vector_store = VectorStore()

            vector_store.clear_database()

            # Clear Session State
            st.session_state.summary = None
            st.session_state.results = None
            st.session_state.comparison = None
            st.session_state.gap_report = None
            st.session_state.chat_history = []
            st.session_state.processed = False
            st.session_state.uploaded_files = []

            st.success("Knowledge Base Cleared!")

            st.rerun()
