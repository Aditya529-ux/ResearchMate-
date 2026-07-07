import streamlit as st
from core.vector_store import VectorStore
from core.document_service import DocumentService


def sidebar():

    with st.sidebar:

        st.header("📂 Documents")

        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=["pdf"],
            accept_multiple_files=True
        )
        st.session_state.uploaded_files = uploaded_files

        process = st.button("Process Documents")

        if process:

            if not uploaded_files:
                st.warning("Please upload at least one PDF.")
            else:

                with st.spinner("Processing PDFs..."):

                    service = DocumentService()



                    summary = service.process_documents(uploaded_files)
                    st.session_state.summary = summary

                st.session_state.processed = True


                st.success(
                            f"""
                        Processed Successfully!

                        📄 Papers : {summary['papers']}

                        🧩 Chunks : {summary['chunks']}
                        """
                        )

                st.balloons()

        st.divider()

        st.subheader("📚 Knowledge Base")

        if "summary" in st.session_state:

            summary = st.session_state.summary

            st.success("🟢 Ready")

            st.metric(
                "Indexed Papers",
                summary["papers"]
            )

            st.metric(
                "Stored Chunks",
                summary["chunks"]
            )

        else:

            st.warning("No documents processed.")


        st.divider()

        st.subheader("Uploaded Papers")

        if uploaded_files:

            for file in uploaded_files:

                st.success(f"📄 {file.name}")

        else:

            st.info("No uploaded papers.")


        if st.button("🗑 Reset Knowledge Base"):

            self_clear = VectorStore()

            self_clear.clear_database()

            st.session_state.pop(
                "summary",
                None
            )

            st.success(
                "Knowledge Base Cleared!"
            )

            st.rerun()
