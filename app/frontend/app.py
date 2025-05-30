import streamlit as st
import requests

st.set_page_config(page_title="Meeting Transcript Summarizer")

st.title("📄 Meeting Transcript Summarizer")
st.write("Upload a meeting transcript to generate a summary and action items.")

uploaded_file = st.file_uploader("Upload a transcript (.txt)", type=["txt"])

if uploaded_file:
    transcript_text = uploaded_file.read().decode("utf-8")
    st.subheader("📜 Transcript Preview")
    st.text_area("Transcript", transcript_text, height=300)

    if st.button("Summarize"):
        with st.spinner("Sending to backend..."):
            # ✅ Fix: Send encoded content as binary
            files = {'file': ('transcript.txt', transcript_text.encode('utf-8'))}

            try:
                response = requests.post("http://127.0.0.1:8000/summarize", files=files)
                response.raise_for_status()
                result = response.json()

                st.subheader("📌 Summary")
                st.write(result["summary"])

                st.subheader("✅ Action Items")
                for item in result["action_items"]:
                    st.markdown(f"- **{item['task']}** → {item['assigned_to']}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to get response from backend: {e}")
