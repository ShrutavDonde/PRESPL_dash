import streamlit as st
import pandas as pd
import plotly.express as px

# Enable wide layout
st.set_page_config(layout="wide")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.sidebar.header("Filter Options")
    
    zones = st.sidebar.multiselect("Select Zone", df["Zone/Segment"].unique())
    verticals = st.sidebar.multiselect("Select Business Vertical", df["Business Vertical"].unique())
    
    filtered_df = df.copy()
    if zones:
        filtered_df = filtered_df[filtered_df["Zone/Segment"].isin(zones)]
    if verticals:
        filtered_df = filtered_df[filtered_df["Business Vertical"].isin(verticals)]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💼 DrTotal by Business Vertical")
        pie1_data = filtered_df.groupby('Business Vertical')['DrTotal'].sum().reset_index()
        fig1 = px.pie(pie1_data, values='DrTotal', names='Business Vertical', title="By Business Vertical")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("🌍 DrTotal by Zone/Segment")
        pie2_data = filtered_df.groupby('Zone/Segment')['DrTotal'].sum().reset_index()
        fig2 = px.pie(pie2_data, values='DrTotal', names='Zone/Segment', title="By Zone/Segment")
        st.plotly_chart(fig2, use_container_width=True)

    # Horizontal divider
    st.markdown("---")

    # Show full filtered table
    st.subheader("📄 Filtered Data Table")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("Please upload a file to view the charts and data.")
