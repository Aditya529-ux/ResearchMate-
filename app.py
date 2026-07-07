import streamlit as st

from ui.pages import home_page


def main():

    st.set_page_config(
        page_title="ResearchMate",
        page_icon="📚",
        layout="wide"
    )

    home_page()


if __name__ == "__main__":
    main()
