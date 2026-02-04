import streamlit as st

st.set_page_config(
    page_title="This is my test app",
    page_icon="😍",
)

st.title("Main Page")
st.sidebar.success("Select a page from above")