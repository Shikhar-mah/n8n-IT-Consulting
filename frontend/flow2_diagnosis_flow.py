import streamlit as st
import requests

N8N_WEBHOOK_URL = "https://viditlimje.app.n8n.cloud/webhook/issue-diagnosis"

def render():
    st.header(":hammer_and_wrench: Issue Diagnosis")

    with st.form("issue_form"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        issue_description = st.text_area("Issue Description")

        submit = st.form_submit_button("Submit Issue")

    if submit:

        if not full_name or not email or not issue_description:
            st.error("Please fill all required fields.")
            return

        payload = {
            "full_name": full_name,
            "email": email,
            "issue_description": issue_description
        }

        try:
            with st.spinner("Analyzing issue..."):
                res = requests.post(N8N_WEBHOOK_URL, data=payload, timeout=60)

            if res.status_code != 200:
                st.error("Request failed (backend error).")
                st.write(res.text)
                return

            raw = res.json()

            # ✅ Validate response structure
            if not isinstance(raw, list) or len(raw) == 0:
                st.success("Response")
                st.json(raw)
                return

            response = raw[0]

            # ✅ Non-IT Case
            if response.get("Category") == "Non-IT":
                st.success("This is not an IT issue")
                st.write(response.get("Solution", "No solution provided."))
                return

            # ✅ IT Issue Case
            if "troubleshooting_steps" in response:
                steps_text = response["troubleshooting_steps"]
                steps_list = [s.strip() for s in steps_text.split("\n") if s.strip()]

                st.success(":white_check_mark: Diagnosis Complete")
                st.subheader(":toolbox: Recommended Steps")

                if steps_list:
                    for i, step in enumerate(steps_list, 1):
                        st.markdown(f"**Step {i}:** {step}")
                else:
                    st.write("No troubleshooting steps provided.")
                return

            # ⚠️ Unexpected Structure
            st.warning("Unexpected response from backend.")
            st.json(raw)

        except Exception as e:
            st.error("Could not connect to n8n webhook.")
            st.write(str(e))
