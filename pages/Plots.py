import streamlit as st
import pandas as pd
import plotly.express as px

# Enable wide layout
st.set_page_config(layout="wide")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.sidebar.header("Filter Options")
    
    zones = st.sidebar.multiselect("Select Zone", df["Zone/Intercompany"].unique())
    verticals = st.sidebar.multiselect("Select Business Vertical", df["Business Vertical"].unique())
    locations = st.sidebar.multiselect("Select Location", df["Location"].unique())
    ratings = st.sidebar.multiselect("Select Rating", df["Rating"].unique())
    
    filtered_df = df.copy()
    if zones:
        filtered_df = filtered_df[filtered_df["Zone/Intercompany"].isin(zones)]
    if verticals:
        filtered_df = filtered_df[filtered_df["Business Vertical"].isin(verticals)]
    if locations:
        filtered_df = filtered_df[filtered_df['Location'].isin(locations)]
    if ratings:
        filtered_df = filtered_df[filtered_df['Rating'].isin(ratings)]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💼 Outstanding (Dr-Cr) by Business Vertical")
        grouped1 = filtered_df.groupby('Business Vertical')[['DrTotal', 'CrTotal']].sum().reset_index()
        grouped1['Outstanding (Dr-Cr)'] = grouped1['DrTotal'] - grouped1['CrTotal']
        fig1 = px.pie(grouped1, values='Outstanding (Dr-Cr)', names='Business Vertical', title="By Business Vertical")
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("📍 Outstanding (Dr-Cr) by Location")
        grouped2 = filtered_df.groupby('Location')[['DrTotal', 'CrTotal']].sum().reset_index()
        grouped2['Outstanding (Dr-Cr)'] = grouped2['DrTotal'] - grouped2['CrTotal']
        fig2 = px.pie(grouped2, values='Outstanding (Dr-Cr)', names='Location', title="By Location")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.subheader("🌍 Outstanding (Dr-Cr) by Zone/Intercompany")
        grouped3 = filtered_df.groupby('Zone/Intercompany')[['DrTotal', 'CrTotal']].sum().reset_index()
        grouped3['Outstanding (Dr-Cr)'] = grouped3['DrTotal'] - grouped3['CrTotal']
        fig3 = px.pie(grouped3, values='Outstanding (Dr-Cr)', names='Zone/Intercompany', title="By Zone/Intercompany")
        st.plotly_chart(fig3, use_container_width=True)

        st.subheader("⭐ Outstanding (Dr-Cr) by Rating")
        grouped4 = filtered_df.groupby('Rating')[['DrTotal', 'CrTotal']].sum().reset_index()
        grouped4['Outstanding (Dr-Cr)'] = grouped4['DrTotal'] - grouped4['CrTotal']
        fig4 = px.pie(grouped4, values='Outstanding (Dr-Cr)', names='Rating', title="By Rating")
        st.plotly_chart(fig4, use_container_width=True)

    # Horizontal divider
    st.markdown("---")

    # Show full filtered table
    st.subheader("📄 Filtered Data Table")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("Please upload a file to view the charts and data.")
