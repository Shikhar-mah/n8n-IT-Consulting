import streamlit as st
import requests

N8N_BASE_URL = "https://your-n8n-instance/webhook"

def render():
    st.header("Asset Lifecycle & Replacement Recommendation")

    asset_tag = st.text_input("Enter Asset Tag")

    if st.button("Analyze Asset Lifecycle"):
        payload = {"asset_tag": asset_tag}

        response = requests.post(f"{N8N_BASE_URL}/lifecycle", json=payload)

        if response.status_code == 200:
            result = response.json()
            st.json(result)
        else:
            st.error("Analysis failed")
