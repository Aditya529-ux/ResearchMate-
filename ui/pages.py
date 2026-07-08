import streamlit as st
import pandas as pd

from ui.components import sidebar
from ui.chat import render_chat

from core.retriever import Retriever
from core.qa_engine import QAEngine
from core.comparison_engine import ComparisonEngine
from core.gap_finder import GapFinder


# --------------------------------------------------
# Session State
# --------------------------------------------------

def initialize_session():

    defaults = {

        #"quick_prompt": None,

        "summary": None,

        "results": None,

        "comparison": None,

        "gap_report": None,

        "answer": None,

        "chat_history": [],

        "uploaded_files": [],

        "processed": False,

        "page": "💬 Research Assistant"

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# --------------------------------------------------
# Home Page
# --------------------------------------------------

def home_page():

    initialize_session()

    # ================= Hero ================= #

    st.markdown(
        """
    <div style="text-align:center; padding:30px 0 15px 0;">

    <h1 style="font-size:64px; margin-bottom:10px;">
    📚 ResearchMate
    </h1>

    <h3 style="color:#d1d5db; font-weight:500; margin-top:0;">
    AI-powered Multi-Paper Research Assistant
    </h3>

    <p style="color:#9ca3af; font-size:16px; margin-top:8px;">
    Powered by
    <b>Gemini 2.5 Flash</b>
    •
    <b>ChromaDB</b>
    •
    <b>Sentence Transformers</b>
    </p>

    </div>
    """,
        unsafe_allow_html=True
    )

    # ================= Sidebar ================= #

    sidebar()

    page = st.session_state.get(
        "page",
        "💬 Research Assistant"
    )

    # ======================================================
    # PAGE : RESEARCH ASSISTANT
    # ======================================================

    if page == "💬 Research Assistant":

        # ---------- Welcome ---------- #

        if not st.session_state.processed:

            st.info(
                """
## 👋 Welcome to ResearchMate

Upload one or more research papers from the sidebar.

### 🚀 Features

- 💬 Ask questions across papers

- 📊 Compare research papers

- 🔍 Discover research gaps

- 📚 AI-powered retrieval

---

### ⬅ Start by uploading PDF research papers.
"""
            )

            st.stop()

       # ---------- Quick Start ---------- #

        if len(st.session_state.chat_history) == 0:

            st.markdown("## 👋 How can I help today?")

            st.caption(
                "Here are some example questions you can ask ResearchMate."
            )

            col1, col2 = st.columns(2)

            with col1:

                with st.container(border=True):
                    st.markdown("### 📄 Summarize Papers")
                    st.caption(
                        "Summarize all uploaded research papers."
                    )

                with st.container(border=True):
                    st.markdown("### 📊 Compare Methodologies")
                    st.caption(
                        "Compare the methodologies used in the uploaded papers."
                    )

            with col2:

                with st.container(border=True):
                    st.markdown("### 🔍 Find Research Gaps")
                    st.caption(
                        "Identify future research opportunities."
                    )

                with st.container(border=True):
                    st.markdown("### 🧠 Best Performing Paper")
                    st.caption(
                        "Determine which paper reports the strongest results."
                    )

            st.divider()
    # --------------------------------------------------
    # Chat Input
    # --------------------------------------------------

    question = render_chat()

    # Use quick prompt if one was selected


    # --------------------------------------------------
    # Generate Answer
    # --------------------------------------------------

    if question:

        with st.spinner("🧠 ResearchMate is analyzing your papers..."):

            retriever = Retriever()

            results = retriever.retrieve(question)
            

            st.session_state.results = results

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
                results["documents"][0],
                results["metadatas"][0]
            )

            st.session_state.chat_history.append(

                {

                    "question": question,

                    "answer": answer["answer"],

                    "sources": answer["sources"]

                }

            )

            st.session_state.answer = answer

    # --------------------------------------------------
    # Conversation
    # --------------------------------------------------

    if st.session_state.chat_history:

        st.markdown("## 💬 Conversation")

        for chat in st.session_state.chat_history:

            with st.chat_message("user"):

                st.write(chat["question"])

            with st.chat_message("assistant"):

                st.write(chat["answer"])

                if chat["sources"]:

                    st.caption("Sources")

                    for source in chat["sources"]:

                        st.markdown(f"- 📄 **{source}**")

    # --------------------------------------------------
    # Retrieved Chunks
    # --------------------------------------------------

    results = st.session_state.get("results")

    if results and results["found"]:

        documents = results["documents"][0]

        metadatas = results["metadatas"][0]

        with st.expander("📚 View Retrieved Chunks"):

            for document, metadata in zip(documents, metadatas):

                st.markdown(f"### 📄 {metadata['paper']}")

                st.caption(

                    f"Chunk {metadata['chunk_id']}"

                )

                st.write(document)

                st.divider()

    # ======================================================
    # PAGE : PAPER COMPARISON
    # ======================================================

    elif page == "📊 Compare Papers":

        st.markdown("## 📊 Paper Comparison")

        st.caption(
            "Compare all uploaded research papers side-by-side."
        )

        if st.button(
            "📊 Generate Comparison",
            use_container_width=True
        ):

            with st.spinner("Generating comparison..."):

                engine = ComparisonEngine()

                st.session_state.comparison = (
                    engine.compare_papers()
                )

        comparison = st.session_state.get("comparison")

        if comparison is None:

            st.info(
                """
No comparison has been generated yet.

Click **Generate Comparison** to compare your uploaded papers.
"""
            )

        else:

            st.dataframe(
                comparison,
                use_container_width=True
            )

            df = pd.DataFrame(comparison)

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(

                "⬇ Download Comparison CSV",

                data=csv,

                file_name="ResearchMate_Comparison.csv",

                mime="text/csv"

            )

    # ======================================================
    # PAGE : RESEARCH GAPS
    # ======================================================

    elif page == "🔍 Research Gaps":

        st.markdown("## 🔍 Research Gap Analysis")

        st.caption(
            "Discover unexplored opportunities and future research directions."
        )

        if st.button(

            "🔍 Analyze Research Collection",

            use_container_width=True

        ):

            with st.spinner("Analyzing research collection..."):

                finder = GapFinder()

                st.session_state.gap_report = (

                    finder.analyze()

                )

        report = st.session_state.get("gap_report")

        if report is None:

            st.info(
                """
No research gap report available.

Click **Analyze Research Collection**
to generate AI-powered insights.
"""
            )

        else:

            with st.container(border=True):

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

                st.divider()

                st.write(report["message"])

    # ======================================================
    # Footer
    # ======================================================

    st.divider()

    st.caption(
        "📚 ResearchMate v3 • Powered by Gemini 2.5 Flash • ChromaDB • Sentence Transformers"
    )
