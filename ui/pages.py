import streamlit as st
from ui.components import sidebar
from ui.chat import render_chat
from core.retriever import Retriever
from core.qa_engine import QAEngine
from core.comparison_engine import ComparisonEngine
from core.gap_finder import GapFinder


# --------------------------------------------------
# Initialize Session State
# --------------------------------------------------

def initialize_session():

    defaults = {
        "summary": None,
        "results": None,
        "comparison": None,
        "gap_report": None,
        "answer": None,
        "chat_history": [],
        "uploaded_files": [],
        "processed": False,
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# --------------------------------------------------
# Home Page
# --------------------------------------------------

def home_page():

    initialize_session()

    st.title("📚 ResearchMate")
    st.markdown("### Multi-Paper Research Assistant")

    # ================= Sidebar ================= #

    sidebar()

    # ================= Tabs ================= #

    tab1, tab2, tab3 = st.tabs(
        [
            "💬 Ask ResearchMate",
            "📊 Compare Papers",
            "🔍 Research Gaps"
        ]
    )

    # ================= Tab 1: Ask ResearchMate ================= #

    with tab1:

        st.divider()

        question = render_chat()

        if question:

            if not question.strip():

                st.warning("Please enter a question.")

            else:

                with st.spinner("🧠 ResearchMate is analyzing your papers..."):

                    retriever = Retriever()

                    results = retriever.retrieve(question)

                    st.session_state.results = results

                    documents = results["documents"][0]

                    metadatas = results["metadatas"][0]

                    qa = QAEngine()

                    answer = qa.answer_question(

                        question,

                        documents,

                        metadatas

                    )
                    st.toast("✅ Answer Generated")
                st.session_state.last_question = question
                st.session_state.answer = answer
                st.session_state.chat_history.append(
                    {
                        "question": question,
                        "answer": answer["answer"],
                        "sources": answer["sources"]
                    }
                )

        # ---------- AI Answer ---------- #

        for chat in st.session_state.chat_history:

            with st.chat_message("user"):

                st.write(chat["question"])

            with st.chat_message("assistant"):

                st.write(chat["answer"])

                st.markdown("#### 📚 Sources")

                for paper in chat["sources"]:

                    st.markdown(f"- 📄 **{paper}**")

        # ---------- Retrieved Chunks ---------- #

        results = st.session_state.get("results", None)

        if results is not None:

            documents = results.get("documents", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]

            st.divider()

            st.success(f"Found {len(documents)} relevant chunks.")

            st.subheader("📄 Retrieved Chunks")

            for document, metadata in zip(documents, metadatas):

                paper_name = metadata.get("paper", "Unknown Paper")

                st.markdown(f"### 📄 {paper_name}")

                st.caption(
                    f"Chunk {metadata.get('chunk_id', '-')}"
                )

                preview = document[:250]

                if len(document) > 250:
                    st.write(preview + "...")
                else:
                    st.write(document)

                with st.expander("📖 Read Full Chunk"):
                    st.write(document)

                st.divider()

    # ================= Tab 2: Compare Papers ================= #

    with tab2:

        st.subheader("📊 Compare Research Papers")

        if st.button("Compare Papers"):

            engine = ComparisonEngine()

            st.session_state.comparison = engine.compare_papers()

        comparison = st.session_state.get("comparison")

        if comparison is not None:

            st.table(comparison)

    # ================= Tab 3: Research Gaps ================= #

    with tab3:

        st.subheader("🔍 Research Gap Analysis")

        if st.button("Analyze Research Collection"):

            finder = GapFinder()

            st.session_state.gap_report = finder.analyze()

        report = st.session_state.get("gap_report")

        if report is not None:

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
