import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.dataframe(df)
else:
    st.info("Please upload a file to view the table.")
