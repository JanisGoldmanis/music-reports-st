import streamlit as st



st.set_page_config(layout="wide")



pages = {
    "Songs": [
        st.Page("data.py", title="Songs"),
        st.Page("upload_file.py", title="Upload"),
    ],
    "Process Files": [
        st.Page("account.py", title="Account"),
        st.Page("example.py", title="Example"),
    ],
}

pg = st.navigation(pages)
pg.run()