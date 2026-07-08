import streamlit as st


def initialize_session():

    defaults = {

        "summary": None,

        "results": None,

        "comparison": None,

        "gap_report": None,

        "answer": None,

        "chat_history": [],

        "uploaded_files": [],

        "processed": False
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value
