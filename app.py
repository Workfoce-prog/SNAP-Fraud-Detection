
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_authenticator as stauth
from yaml import safe_load

# ---- User Authentication ----
names = ['Investigator One', 'Supervisor Two']
usernames = ['investigator1', 'supervisor2']
passwords = ['snap2025', 'review2025']

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    'fraud_dashboard', 'abcdef', cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status is False:
    st.error('Invalid username or password')
elif authentication_status is None:
    st.warning('Please enter your username and password')
elif authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.success(f"Welcome {name}!")

    st.title("🕵️ SNAP Fraud Detection Dashboard")

    @st.cache_data
    def load_data():
        return pd.read_csv("SNAP_Fraud_Metrics_Dashboard.csv")

    df = load_data()

    st.markdown("### 🔍 Browse SNAP Fraud Detection Cases")
    st.dataframe(df)

    st.markdown("### 📊 Highest SNAP Fraud Risk Scores by County")
    fig = px.bar(df.sort_values(by="SNAP_FRAUD_SCORE", ascending=False),
                x="County", y="SNAP_FRAUD_SCORE", color="SNAP_FRAUD_SCORE",
                title="Fraud Score Distribution by County")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📈 Fraud Score Distribution")
    fig2 = px.histogram(df, x="SNAP_FRAUD_SCORE", nbins=10, title="Distribution of SNAP Fraud Scores")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 🧠 Score Interpretation & Recommendations")
    with st.expander("Click to view fraud score interpretations"):
        st.markdown("""
- **0–59** 🟢: Low Risk – Routine monitoring  
- **60–79** 🟠: Moderate Risk – Targeted review  
- **80–100+** 🔴: High Risk – Flag for full investigation and audit
""")

    st.download_button(
        label="📥 Download Full Dataset (CSV)",
        data=df.to_csv(index=False),
        file_name="SNAP_Fraud_Metrics_Dashboard.csv",
        mime="text/csv"
    )
