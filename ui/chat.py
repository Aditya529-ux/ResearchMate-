import streamlit as st


def render_chat():

    st.subheader("💬 Ask ResearchMate")

    question = st.chat_input(
        "Ask anything about your research papers..."
    )

    return question
