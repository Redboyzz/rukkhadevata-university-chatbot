import streamlit as st

from src.chatbot import get_answer, load_faqs, prepare_matcher

st.set_page_config(
    page_title="Rukkhadevata University Enquiry",
    page_icon="🎓",
    layout="centered",
)

st.title("🎓 Rukkhadevata University")
st.subheader("College Enquiry Chatbot")
st.info(
    "**Fictional demonstration:** Rukkhadevata University and all college details in this app are sample content. "
    "They do not describe a real institution."
)
st.caption("Ask about courses, admissions, documents, timings, scholarships, the library, exams, or hostel facilities.")

faqs = load_faqs()
matcher = prepare_matcher(faqs)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm the Rukkhadevata University demo enquiry assistant. What would you like to know?",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Type your college enquiry")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    answer = get_answer(question, faqs, matcher)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
