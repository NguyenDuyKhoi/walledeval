# app.py
import streamlit as st
import pandas as pd

# Fake data demo
reports = pd.DataFrame([
    {"Test Name": "Jailbreak Prompt #1", "Model": "GPT-4", "Type": "Jailbreak", "Result": "Fail", "Date": "2026-06-15"},
    {"Test Name": "Bias Check #3", "Model": "Claude", "Type": "Bias", "Result": "Pass", "Date": "2026-06-14"},
    {"Test Name": "Harmful Prompt #2", "Model": "GPT-3.5", "Type": "Harmful", "Result": "Warning", "Date": "2026-06-13"},
])

# Sidebar
st.sidebar.title("⚡ walledeval")
st.sidebar.markdown("### Navigation")
page = st.sidebar.radio("Go to:", ["Dashboard", "Run Test", "Reports", "Settings"])

# Dashboard
if page == "Dashboard":
    st.title("📊 Dashboard")
    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Passed", 42)
    col2.metric("❌ Failed", 17)
    col3.metric("⚠️ Warnings", 9)

    st.subheader("Recent Reports")
    st.dataframe(reports)

# Run Test
elif page == "Run Test":
    st.title("🧪 Run New Test")
    prompt = st.text_area("Enter prompt to test:")
    model = st.selectbox("Select Model:", ["GPT-4", "Claude", "GPT-3.5"])
    test_type = st.multiselect("Test Type:", ["Jailbreak", "Harmful", "Bias"])

    if st.button("Run Test"):
        st.success(f"Running test on {model} with {test_type}...")
        st.info("Result: ❌ Fail (demo)")

# Reports
elif page == "Reports":
    st.title("📑 Reports")
    st.dataframe(reports)

# Settings
elif page == "Settings":
    st.title("⚙️ Settings")
    st.text_input("OpenAI API Key")
    st.text_input("Anthropic API Key")
    st.selectbox("Theme:", ["Dark", "Light"])
    st.slider("Risk Threshold", 1, 5, 3)
