import time
import streamlit as st

from core.document_service import DocumentService
from core.vector_store import VectorStore


def sidebar():

    with st.sidebar:

        # ==================================================
        # Branding
        # ==================================================

        st.title("📚 ResearchMate")
        st.caption("AI Research Workspace")

        st.divider()

        # ==================================================
        # Navigation
        # ==================================================

        st.subheader("🧭 Navigation")

        page = st.radio(
            "",
            [
                "💬 Research Assistant",
                "📊 Compare Papers",
                "🔍 Research Gaps"
            ],
            label_visibility="collapsed"
        )

        st.session_state.page = page

        st.divider()

        # ==================================================
        # Upload Documents
        # ==================================================

        st.subheader("📂 Upload Documents")

        uploaded_files = st.file_uploader(
            "Upload PDF Files",
            type=["pdf"],
            accept_multiple_files=True
        )

        if uploaded_files:
            st.session_state.uploaded_files = uploaded_files

        if st.button(
            "⚙️ Process Documents",
            use_container_width=True
        ):

            if not uploaded_files:

                st.warning("Please upload at least one PDF.")

            else:

                progress = st.progress(0)

                status = st.empty()

                status.write("📄 Reading PDF files...")
                progress.progress(20)

                status.write("✂️ Creating chunks...")
                progress.progress(45)

                status.write("🧠 Generating embeddings...")
                progress.progress(75)

                service = DocumentService()

                summary = service.process_documents(
                    uploaded_files
                )

                status.write("💾 Saving Knowledge Base...")
                progress.progress(100)

                time.sleep(0.8)

                progress.empty()
                status.empty()

                st.session_state.summary = summary
                st.session_state.processed = True

                st.success("✅ Documents processed!")

        st.divider()

        # ==================================================
        # Knowledge Base
        # ==================================================

        summary = st.session_state.get("summary")

        with st.container(border=True):

            st.markdown("### 📊 Knowledge Base")

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

                st.caption(
                    "No documents processed yet."
                )

        st.divider()

        # ==================================================
        # Uploaded Files
        # ==================================================

        with st.container(border=True):

            st.markdown("### 📄 Uploaded Files")

            files = st.session_state.get(
                "uploaded_files",
                []
            )

            if files:

                for file in files:

                    st.write(f"✅ {file.name}")

            else:

                st.caption("No uploaded PDFs.")

        st.divider()

        # ==================================================
        # Reset
        # ==================================================

        if st.button(
            "🗑 Reset Knowledge Base",
            use_container_width=True
        ):

            vector_store = VectorStore()

            vector_store.clear_database()

            st.session_state.summary = None
            st.session_state.results = None
            st.session_state.comparison = None
            st.session_state.gap_report = None
            st.session_state.answer = None
            st.session_state.chat_history = []
            st.session_state.uploaded_files = []
            st.session_state.processed = False

            st.success("Knowledge Base Cleared!")

            st.rerun()
