import streamlit as st
from main import summarize_transcript

st.set_page_config(page_title="Meeting Transcript Summarizer")

st.title("📄 Meeting Transcript Summarizer")
st.write("Upload a meeting transcript to generate a summary and action items.")

uploaded_file = st.file_uploader("Upload a transcript (.txt)", type=["txt"])

if uploaded_file:
    transcript = uploaded_file.read().decode("utf-8")
    st.subheader("📜 Transcript Preview")
    st.text_area("Transcript", transcript, height=300)

    if st.button("Summarize"):
        with st.spinner("Generating summary and action items..."):
            result = summarize_transcript(transcript)

        st.subheader("📌 Summary")
        st.write(result["summary"])

        st.subheader("✅ Action Items")
        for item in result["action_items"]:
            st.markdown(f"- **{item['task']}** → {item['assigned_to']}")
