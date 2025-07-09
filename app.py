
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SNAP Fraud Detection Dashboard", layout="wide")
st.title("🕵️ SNAP Fraud Detection Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("SNAP_Fraud_Metrics_Dashboard.csv")

df = load_data()

# Browse Data
st.markdown("### 🔍 Browse SNAP Fraud Detection Cases")
st.dataframe(df)

# Visualize High Risk Scores
st.markdown("### 📊 Highest SNAP Fraud Risk Scores by County")
fig = px.bar(df.sort_values(by="SNAP_FRAUD_SCORE", ascending=False),
             x="County", y="SNAP_FRAUD_SCORE", color="SNAP_FRAUD_SCORE",
             title="Fraud Score Distribution by County")
st.plotly_chart(fig, use_container_width=True)

# Histogram
st.markdown("### 📈 Fraud Score Distribution")
fig2 = px.histogram(df, x="SNAP_FRAUD_SCORE", nbins=10, title="Distribution of SNAP Fraud Scores")
st.plotly_chart(fig2, use_container_width=True)

# Interpretation & Recommendations
st.markdown("### 🧠 Score Interpretation & Recommendations")
with st.expander("Click to view fraud score interpretations"):
    st.markdown("""
- **0–59** 🟢: Low Risk  
  - ✅ No immediate concern. Routine monitoring.
- **60–79** 🟠: Moderate Risk  
  - ⚠️ Recommend targeted review. Cross-check with program data.
- **80–100+** 🔴: High Risk  
  - 🚨 Flag for investigation. Review transaction logs, merchant behavior, and case notes.
    - Prioritize for fraud prevention units
    - Consider temporary benefit freeze until audit complete
    - Alert interagency partners (e.g., Medicaid, UI, housing)
""")

# Download button
st.download_button(
    label="📥 Download Full Dataset (CSV)",
    data=df.to_csv(index=False),
    file_name="SNAP_Fraud_Metrics_Dashboard.csv",
    mime="text/csv"
)

st.sidebar.markdown("Built by StratDesign Solutions")
