import streamlit as st
import requests

N8N_BASE_URL = "https://shikhar-mah.app.n8n.cloud/webhook/knowlegde"

def render():
    st.header("Feedback, Learning & Knowledge Base Update")
    st.subheader("Submit Ticket Feedback")

    with st.form("feedback_form"):
        ticket_id = st.text_input("Ticket ID")
        feedback_rating = st.slider("Rating", 1, 5)
        feedback_comment = st.text_area("Feedback Comment")

        submit = st.form_submit_button("Submit Request")

    if submit:

        # ✅ Basic validation
        if not ticket_id.strip() or not feedback_comment.strip():
            st.error("Please fill all required fields.")
            return

        payload = {
            "ticket_id": ticket_id.strip(),
            "feedback_rating": feedback_rating,
            "feedback_comment": feedback_comment.strip()
        }

        try:
            res = requests.post(N8N_BASE_URL, json=payload, timeout=30)

            if res.status_code != 200:
                st.error(f"Backend error: {res.status_code}")
                st.write(res.text)
                return

            # ✅ Parse JSON safely
            try:
                data = res.json()
            except ValueError:
                st.error("Backend did not return valid JSON.")
                st.write(res.text)
                return

            # ✅ Validate structure
            if isinstance(data, list):
                if len(data) == 0:
                    st.error("Empty response received from backend.")
                    return
                status = data[0].get("Status")
            elif isinstance(data, dict):
                status = data.get("Status")
            else:
                st.error("Unexpected response format from backend.")
                st.write(data)
                return

            # ✅ Handle statuses
            if status == "Less Rating":
                st.info("How can we improve our service? Please write your suggestions below.")
                
                with st.form("improvements_form"):
                    improvements_to_system = st.text_input("Suggestions...")
                    submit_improvements = st.form_submit_button("Submit Improvements")

            elif status == "Success":
                st.success("✅ Feedback Submitted Successfully!")

            elif status == "Rejected":
                st.warning("⚠️ Feedback was not accepted.")
            
            else:
                st.warning("Unexpected response from backend.")
                st.json(data)

        except requests.exceptions.RequestException as e:
            st.error("Could not connect to n8n webhook.")
            st.write(str(e))

        except Exception as e:
            st.error("Unexpected error occurred.")
            st.write(str(e))