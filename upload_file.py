import streamlit as st
from io import StringIO

from report import get_report


uploaded_files = st.file_uploader('Upload file', accept_multiple_files = True)
if uploaded_files is not None:
    for file in uploaded_files:
        # To convert to a string based IO:
        stringio = StringIO(file.getvalue().decode("utf-8"))
        row_list = stringio.getvalue().splitlines()  # Convert to list where each value is a row

        # st.write(row_list)

        df = get_report(row_list)

        if df is None:
            st.write('Not All Songs Known')

        else:

            st.write(file.name)

            print(df)

            # st.write(df)

            st.dataframe(
                df,
                column_config={
                    "name": st.column_config.Column(
                        width=300
                    ),
                    "duration": st.column_config.Column(
                        width=30
                    ),
                    "count": st.column_config.Column(
                        width=30
                    ),
                    "musician": st.column_config.Column(
                        width=200
                    ),
                    "composer": st.column_config.Column(
                        width=200
                    ),
                    "producer": st.column_config.Column(
                        width=200
                    ),
                    "record_company": st.column_config.Column(
                        width=200
                    ),
                }
            )