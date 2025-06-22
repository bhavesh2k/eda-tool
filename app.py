import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Light EDA Tool", layout="wide")
st.title("📊 Exploratory Data Analysis (EDA) Tool")

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    st.subheader("📌 Data Preview")
    st.dataframe(df.head())

    st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")

    # 👇 Column Selector
    st.subheader("🔧 Select Columns for Analysis")
    selected_cols = st.multiselect("Choose columns to analyze", options=df.columns.tolist(), default=df.columns.tolist())

    if not selected_cols:
        st.warning("Please select at least one column.")
        st.stop()

    df_selected = df[selected_cols]

    st.subheader("📊 Summary Statistics")
    st.dataframe(df_selected.describe(include='all').T)

    st.subheader("🧮 Missing Values")
    missing = df_selected.isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        fig = px.bar(x=missing.index, y=missing.values,
                     labels={'x': 'Columns', 'y': 'Missing Count'},
                     title="Missing Values per Column")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No missing values found.")

    st.subheader("📈 Correlation Heatmap (Numeric)")
    numeric_df = df_selected.select_dtypes(include='number')
    if numeric_df.shape[1] >= 2:
        corr = numeric_df.corr()
        fig = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough numeric columns selected.")

    st.subheader("📊 Categorical Value Counts")
    cat_cols = df_selected.select_dtypes(include='object').columns
    if len(cat_cols) == 0:
        st.info("No categorical columns selected.")
    else:
        for col in cat_cols:
            st.markdown(f"**{col}**")
            vc = df_selected[col].value_counts().head(10)
            fig = px.bar(x=vc.index, y=vc.values, labels={'x': col, 'y': 'Count'})
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("🚨 Numeric Outlier Detection (IQR Method)")

    if numeric_df.shape[1] == 0:
        st.info("No numeric columns selected.")
    else:
        outlier_summary = {}
        for col in numeric_df.columns:
            q1 = numeric_df[col].quantile(0.25)
            q3 = numeric_df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = numeric_df[(numeric_df[col] < lower_bound) | (numeric_df[col] > upper_bound)]
            outlier_summary[col] = len(outliers)

        outlier_df = pd.DataFrame({
            "Column": list(outlier_summary.keys()),
            "Outlier Count": list(outlier_summary.values())
        }).sort_values(by="Outlier Count", ascending=False)

        st.dataframe(outlier_df)

        st.subheader("📦 Box Plots (Optional)")
        box_cols = st.multiselect("Select columns to plot boxplots", options=numeric_df.columns.tolist())

        for col in box_cols:
            fig = px.box(numeric_df, y=col, title=f"Box Plot: {col}")
            st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload a CSV or Excel file to begin.")
