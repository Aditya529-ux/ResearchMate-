import streamlit as st

from ui.components import sidebar


def home_page():

    st.title("📚 ResearchMate")

    st.markdown(
        "### Multi-Paper Research Assistant"
    )

    sidebar()

    st.divider()

    st.subheader("Ask a Question")

    st.text_input(
        "Enter your question",
        placeholder="Example: What datasets are used?"
    )

    st.button("Ask")
