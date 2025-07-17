import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Customer Insights", layout="wide")

st.title("📊 Zone & Business Vertical Analysis")

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Check necessary columns
    required_columns = ['Zone/Segment', 'Business Vertical', 'DrTotal']
    if not all(col in df.columns for col in required_columns):
        st.error("Your file must contain columns: Zone/Segment, Business Vertical, and DrTotal")
    else:
        # --- SIDEBAR FILTERS ---
        st.sidebar.header("🔍 Filter Data")

        # Unique values for filters
        selected_zone = st.sidebar.multiselect(
            "Select Zone/Segment", options=df['Zone/Segment'].dropna().unique(), default=None
        )
        selected_vertical = st.sidebar.multiselect(
            "Select Business Vertical", options=df['Business Vertical'].dropna().unique(), default=None
        )

        # Apply filters
        filtered_df = df.copy()
        if selected_zone:
            filtered_df = filtered_df[filtered_df['Zone/Segment'].isin(selected_zone)]
        if selected_vertical:
            filtered_df = filtered_df[filtered_df['Business Vertical'].isin(selected_vertical)]

        # --- MAIN PAGE PIE CHARTS ---
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
else:
    st.info("Please upload an Excel file to begin.")
