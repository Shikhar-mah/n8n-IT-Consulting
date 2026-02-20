import streamlit as st
import requests
import re

N8N_FLOW1_URL = "https://munkss.app.n8n.cloud/webhook/laptop-request"

def render():
    st.header("💻 Laptop Inventory Request (Flow 1)")
    st.write("Submit a request. The system will approve/reject based on current stock.")

    with st.form("laptop_request_form"):

        # --- Name ---
        user_name = st.text_input("User Name", placeholder="Enter your name")
        name_error = None
        if user_name and not re.match(r"^[A-Za-z ]{2,50}$", user_name.strip()):
            name_error = "Name must contain only letters and spaces (2–50 characters)."
        if name_error:
            st.caption(f"⚠️ {name_error}")

        # --- Email ---
        user_email = st.text_input("User Email", placeholder="example@bluealtair.com")
        email_error = None
        if user_email and not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", user_email.strip()):
            email_error = "Please enter a valid email address."
        if email_error:
            st.caption(f"⚠️ {email_error}")

        # --- Laptop Type ---
        laptop_type = st.selectbox("Laptop Type", ["Dell", "HP", "Lenovo", "MacBook"])

        # --- Quantity ---
        requested_quantity = st.number_input("Requested Quantity", min_value=1, step=1)
        qty_error = None
        if requested_quantity < 1:
            qty_error = "Quantity must be at least 1."
        if qty_error:
            st.caption(f"⚠️ {qty_error}")

        submit = st.form_submit_button("Submit Request")

    if submit:

        # Required field validation
        has_error = False

        if not user_name.strip():
            st.error("User Name is required.")
            has_error = True

        if not user_email.strip():
            st.error("User Email is required.")
            has_error = True

        if name_error or email_error or qty_error:
            has_error = True

        if has_error:
            return

        payload = {
            "user_name": user_name.strip(),
            "user_email": user_email.strip(),
            "laptop_type": laptop_type,
            "requested_quantity": int(requested_quantity),
        }

        try:
            res = requests.post(N8N_FLOW1_URL, json=payload, timeout=60)

            if res.status_code != 200:
                st.error("Request failed (backend error).")
                st.write(res.text)
                return

            data = res.json()

            if data.get("Status") == "Approved":
                st.success("✅ Request Approved!")
                st.markdown(
                    f"""
                    **Laptop Type:** {data.get("Laptop_Type")}  
                    **Quantity Requested:** {data.get("Requested_Quantity")}  
                    """
                )

            elif data.get("Status") == "Rejected":
                st.warning("⚠️ Request Processing (Currently Out of Stock)")
                st.markdown(
                    f"""
                    **Laptop Type:** {data.get("Laptop_Type")}  
                    **Quantity Requested:** {data.get("Requested_Quantity")}  
                    """
                )

            else:
                st.warning("Unexpected response from backend.")
                st.json(data)

        except requests.exceptions.RequestException as e:
            st.error("Could not connect to n8n webhook.")
            st.write(str(e))