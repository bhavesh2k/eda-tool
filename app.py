import streamlit as st
import pandas as pd
import sweetviz as sv
import plotly.express as px
from streamlit.components.v1 import html
import tempfile
import os

st.set_page_config(page_title="EDA Tool", layout="wide")
st.title("🔍 Exploratory Data Analysis (EDA) Tool")

uploaded_file = st.file_uploader("Upload your file (CSV or Excel)", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    file_ext = uploaded_file.name.split(".")[-1]

    try:
        if file_ext in ["xlsx", "xls"]:
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"❌ Failed to read file: {e}")
        st.stop()

    st.subheader("📌 Data Preview")
    st.dataframe(df.head())

    st.subheader("📊 Sweetviz Report")
    with st.spinner("Generating Sweetviz report..."):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp_file:
            report = sv.analyze(df)
            report.show_html(filepath=tmp_file.name, open_browser=False)

        # Read and display the report
        with open(tmp_file.name, 'r', encoding='utf-8') as f:
            html_content = f.read()
            html(html_content, height=1000, scrolling=True)

    st.subheader("📉 Missing Values")
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        fig = px.bar(x=missing.index, y=missing.values,
                     labels={'x': 'Columns', 'y': 'Missing Values'},
                     title="Missing Values per Column")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("✅ No missing values found.")

    st.subheader("📈 Correlation Matrix")
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.shape[1] >= 2:
        corr = numeric_df.corr()
        fig = px.imshow(corr, text_auto=True,
                        color_continuous_scale="RdBu_r",
                        title="Correlation Heatmap")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("❗ Not enough numerical columns for correlation analysis.")
else:
    st.info("👆 Upload a CSV or Excel file to get started.")
