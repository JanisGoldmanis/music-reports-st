import streamlit as st


st.write('Account')

import pandas as pd

data_df = pd.DataFrame(
    {
        "widgets": ["st.selectbox", "st.number_input", "st.text_area", "st.button"],
    }
)

st.dataframe(
    data_df,
    column_config={
        "widgets": st.column_config.Column(
            width="small"
        )
    }
)