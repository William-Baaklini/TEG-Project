# python -m streamlit run app/app.py

import streamlit as st
import requests

st.set_page_config(page_title="Meeting Transcript Summarizer")

st.title("📄 Meeting Transcript Summarizer")
st.write("Upload a meeting transcript to generate a summary and action items.")

uploaded_file = st.file_uploader("Upload a transcript (.txt or .md)", type=["txt", "md"])

if uploaded_file:
    transcript_text = uploaded_file.read().decode("utf-8")
    st.subheader("📜 Transcript Preview")
    st.text_area("Transcript", transcript_text, height=300)

    if st.button("Summarize"):
        with st.spinner("AI is analyzing your file..."):
            # ✅ Fix: Send encoded content as binary
            files = {'file': ('transcript.txt', transcript_text.encode('utf-8'))}

            try:
                response = requests.post("http://127.0.0.1:8000/run", files=files)
                response.raise_for_status()
                result = response.json()

                st.subheader("📌 Summary")
                summary = result.get("summary", "")
                st.write(summary)

                actions_data = result.get("actions", {})
                action_items = actions_data.get("action_items", [])
                action_summary = actions_data.get("summary", {})

                if action_items:
                    st.subheader("✅ Action Items")
                    for item in action_items:
                        st.markdown(f"""
                        **📝 {item['description']}**
                        - 👤 Assigned to: `{item['assigned_to']}`
                        - 📌 Priority: `{item['priority']}`
                        - 🕒 Due date: `{item['due_date']}`
                        - 💬 Context: {item['context']}
                        - 🧠 Reason: {item['assignment_reason']}
                        """)
                else:
                    st.info("No action items found.")

                if action_summary:
                    st.subheader("📊 Action Items Summary")
                    st.markdown(f"""
                    - Total: **{action_summary.get("total_action_items", 0)}**
                    - People involved: {', '.join(action_summary.get("people_with_assignments", []))}
                    - Priority breakdown:
                        - 🔴 High: {action_summary.get("priority_breakdown", {}).get("high", 0)}
                        - 🟡 Medium: {action_summary.get("priority_breakdown", {}).get("medium", 0)}
                        - 🟢 Low: {action_summary.get("priority_breakdown", {}).get("low", 0)}
                    """)
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to get response from backend: {e}")
