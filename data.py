import streamlit as st
import pandas as pd

file = 'data/songs.csv'
df = pd.read_csv(file, encoding='latin1')

# Editable table
edited_df = st.data_editor(df, num_rows="dynamic")

# Use edited DataFrame
st.write("Updated DataFrame:")
st.write(edited_df)