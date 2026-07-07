import streamlit as st

from ui.components import sidebar
from core.retriever import Retriever
from core.comparison_engine import ComparisonEngine


def home_page():

    st.title("📚 ResearchMate")

    st.markdown(
        "### Multi-Paper Research Assistant"
    )

    sidebar()
    st.divider()

    st.subheader("📊 Paper Comparison")
    if st.button("Compare Papers"):

        if "uploaded_files" not in st.session_state:

            st.warning("Upload papers first.")

        else:

            engine = ComparisonEngine()

            table = engine.compare_papers(
                st.session_state.uploaded_files
            )

            st.table(table)



    st.divider()

    st.subheader("Ask a Question")

    question = st.text_input(
        "Enter your question",
        placeholder="Example: What datasets are used?"
    )

    ask = st.button("Ask")

    if ask:

        if not question.strip():
            st.warning("Please enter a question.")
            return

        with st.spinner("Searching documents..."):

            retriever = Retriever()

            results = retriever.retrieve(question)

        st.success("Relevant Chunks Retrieved!")

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        st.divider()
        st.success(
            f"Found {len(documents)} relevant chunks."
        )

        st.subheader("Retrieved Chunks")

        for i, (document, metadata) in enumerate(zip(documents, metadatas), start=1):

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


