
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SNAP Fraud Detection Dashboard", layout="wide")
st.title("🕵️ SNAP Fraud Detection Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("SNAP_Fraud_Metrics_Dashboard.csv")

df = load_data()

st.markdown("### 🔍 Browse Fraud Detection Cases")
st.dataframe(df)

# Visualization: Fraud score by county
st.markdown("### 📊 Highest Fraud Risk Scores by County")
fig = px.bar(df.sort_values(by="SNAP_FRAUD_SCORE", ascending=False),
             x="County", y="SNAP_FRAUD_SCORE", color="SNAP_FRAUD_SCORE",
             title="Fraud Score Distribution by County")
st.plotly_chart(fig, use_container_width=True)

# Histogram of risk levels
st.markdown("### 🧮 Score Distribution")
fig2 = px.histogram(df, x="SNAP_FRAUD_SCORE", nbins=10, title="SNAP Fraud Score Distribution")
st.plotly_chart(fig2, use_container_width=True)

# Download
st.download_button(
    label="📥 Download Full Dataset (CSV)",
    data=df.to_csv(index=False),
    file_name="SNAP_Fraud_Metrics_Dashboard.csv",
    mime="text/csv"
)

st.sidebar.markdown("Built by StratDesign Solutions")
