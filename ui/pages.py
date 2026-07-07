import streamlit as st
from core.qa_engine import QAEngine

from ui.components import sidebar
from core.retriever import Retriever
from core.comparison_engine import ComparisonEngine
from core.gap_finder import GapFinder


def home_page():

    st.title("📚 ResearchMate")

    st.markdown(
        "### Multi-Paper Research Assistant"
    )

    # ---------------- Sidebar ---------------- #

    sidebar()

    # ---------------- Ask Question ---------------- #

    st.divider()

    st.subheader("💬 Ask ResearchMate")

    question = st.text_input(
        "Enter your question",
        placeholder="Example: What datasets are used?"
    )

    ask = st.button("Ask")

    if ask:

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            with st.spinner("Searching documents..."):

                retriever = Retriever()

                results = retriever.retrieve(question)

                st.session_state.results = results

                documents = results["documents"][0]

                metadatas = results["metadatas"][0]

                qa = QAEngine()

                response = qa.answer_question(
                    question,
                    documents,
                    metadatas
                )

                st.session_state.answer = response

            st.success("Relevant Chunks Retrieved!")


            if "answer" in st.session_state:

                st.divider()

                st.subheader("🤖 ResearchMate Answer")

                st.success(
                    st.session_state.answer["answer"]
                )

                st.markdown("### Sources")

                for paper in st.session_state.answer["sources"]:

                    st.info(f"📄 {paper}")
    # ---------------- Retrieved Chunks ---------------- #

    if "results" in st.session_state:

        documents = st.session_state.results["documents"][0]
        metadatas = st.session_state.results["metadatas"][0]

        st.divider()

        st.success(
            f"Found {len(documents)} relevant chunks."
        )

        st.subheader("📄 Retrieved Chunks")

        for document, metadata in zip(documents, metadatas):

            paper_name = metadata["paper"]

            preview = document[:250]

            st.markdown(f"## 📄 {paper_name}")

            st.caption(
                f"Chunk {metadata['chunk_id']}"
            )

            if len(document) > 250:

                st.write(preview + "...")

            else:

                st.write(document)

            with st.expander("📖 Read Full Chunk"):

                st.write(document)

            st.divider()

    # ---------------- Paper Comparison ---------------- #

    st.subheader("📊 Compare Research Papers")

    if st.button("Compare Papers"):

        engine = ComparisonEngine()

        table = engine.compare_papers()

        st.table(table)

    # ---------------- Gap Finder ---------------- #

    st.divider()

    st.subheader("🔍 Research Gap Analysis")

    if st.button("Analyze Research Collection"):

        finder = GapFinder()

        report = finder.analyze()

        st.success(report["status"])

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Research Papers",
                report["papers"]
            )

        with col2:

            st.metric(
                "Total Chunks",
                report["chunks"]
            )

        st.info(report["message"])
