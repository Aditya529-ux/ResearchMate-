import streamlit as st
from ui.components import sidebar
from ui.chat import render_chat
from core.retriever import Retriever
from core.qa_engine import QAEngine
from core.comparison_engine import ComparisonEngine
from core.gap_finder import GapFinder
import pandas as pd


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

        # ---------------- Paper Selector ---------------- #

        uploaded_files = st.session_state.get("uploaded_files", [])

        paper_options = ["All Papers"] + [
            file.name for file in uploaded_files
        ]

        selected_paper = st.selectbox(
            "📄 Search In",
            paper_options,
            key="paper_selector"
        )

        question = render_chat()

        if question:

            if not question.strip():

                st.warning("Please enter a question.")

            else:

                with st.spinner("🧠 ResearchMate is analyzing your papers..."):

                    retriever = Retriever()

                    if selected_paper == "All Papers":

                        results = retriever.retrieve(question)

                    else:

                        results = retriever.retrieve(
                            question,
                            paper_name=selected_paper
                        )

                    st.session_state.results = results

                    # No relevant chunks found
                    if not results["found"]:

                        answer = {

                            "answer": "❌ I couldn't find relevant information in the uploaded research papers.",

                            "sources": []

                        }

                    else:

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

                if chat["sources"]:

                    st.markdown("#### 📚 Sources")

                    for paper in chat["sources"]:

                        st.caption(f"📄 {paper}")

                    st.markdown(f"- 📄 **{paper}**")

        # ---------- Retrieved Chunks ---------- #

        results = st.session_state.get("results", None)

        if results is not None:

            documents = results.get("documents", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]

            st.divider()

            with st.container(border=True):

                st.markdown("### 📄 Search Results")

                st.write(
                    f"Found **{len(documents)}** relevant papers."
                )


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

            df = pd.DataFrame(comparison)

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(

                "⬇ Download Comparison CSV",

                data=csv,

                file_name="ResearchMate_Comparison.csv",

                mime="text/csv"

            )

    # ================= Tab 3: Research Gaps ================= #

    with tab3:

        st.subheader("🔍 Research Gap Analysis")

        if st.button("Analyze Research Collection"):

            finder = GapFinder()

            st.session_state.gap_report = finder.analyze()

        report = st.session_state.get("gap_report")

        if report is not None:

            with st.container(border=True):

                st.markdown("### 🔍 Research Gap Analysis")

                st.write(report["status"])

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
