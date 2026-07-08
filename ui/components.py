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

                progress = st.progress(0)

                status = st.empty()

                status.write("📄 Reading PDF files...")
                progress.progress(20)

                status.write("✂ Creating chunks...")
                progress.progress(40)

                status.write("🧠 Generating embeddings...")
                progress.progress(70)

                service = DocumentService()

                summary = service.process_documents(uploaded_files)

                status.write("💾 Saving to Knowledge Base...")
                progress.progress(100)

                status.success("✅ Processing Complete!")
                import time

                time.sleep(1)

                progress.empty()

                status.empty()

                # Save everything in Session State
                st.session_state.summary = summary
                st.session_state.processed = True

                st.success("✅ Documents processed successfully!")

        # ---------------- Knowledge Base ---------------- #

        st.divider()

        st.subheader("📚 Knowledge Base")

        summary = st.session_state.get("summary")

        if summary:

            with st.container(border=True):

                st.markdown("### 📚 Knowledge Base")

                st.write("🟢 Ready")

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

            with st.container(border=True):

                st.markdown("### 📚 Knowledge Base")

                st.caption(
                    "Upload papers to begin."
                )

        # ---------------- Uploaded Papers ---------------- #

        st.divider()

        st.subheader("📄 Uploaded Papers")

        files = st.session_state.get("uploaded_files", [])

        if files:

            for file in files:

                st.write(f"✅ {file.name}")

        else:

            with st.container(border=True):

                st.markdown("### 👋 Welcome to ResearchMate")

                st.write(
                    """
        Upload one or more research papers to get started.

        ### 🚀 Quick Start

        1. 📄 Upload PDF research papers

        2. ⚙️ Click **Process Documents**

        3. 💬 Ask questions

        4. 📊 Compare papers

        5. 🔍 Discover research gaps
        """
                )

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
