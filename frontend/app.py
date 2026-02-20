import streamlit as st
import flow1_inventory_flow as inventory_flow
import flow2_diagnosis_flow as diagnosis_flow
import flow5_lifecycle_flow as lifecycle_flow
import flow6_feedback_flow as feedback_flow

st.set_page_config(page_title="AI IT Support Helper", layout="wide")

st.title("AI IT Support Helper")

menu = st.sidebar.selectbox(
    "Select Flow",
    [
        "Laptop Inventory & Availability",
        "Issue Diagnosis",
        "Asset Lifecycle & Replacement Recommendation Flow",
        "Feedback Form"
    ]
)

if menu == "Laptop Inventory & Availability":
    # st.sidebar.text("")
    inventory_flow.render()

elif menu == "Issue Diagnosis":
    diagnosis_flow.render()

elif menu == "Asset Lifecycle":
    lifecycle_flow.render()

elif menu == "Feedback Form":
    feedback_flow.render()
