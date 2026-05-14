import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="IYNI AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 IYNI AI Chatbot")
st.caption("Created by Parthasarathi M — BSc CS with AI Student")
st.divider()

try:
    api_key = st.secrets["GROQ_API_KEY"].strip()
    client = Groq(api_key=api_key)
except Exception:
    st.error("❌ GROQ API key not found. Please check Streamlit Secrets.")
    st.stop()

CREATOR_KEYWORDS = [
    "created you",
    "made you",
    "creator",
    "founder",
    "developer",
    "built you",
    "invented you",
    "who made you",
    "who are you made by"
]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are IYNI, a smart, friendly, and helpful AI chatbot "
                "created by Parthasarathi M, a BSc Computer Science with "
                "Artificial Intelligence student and passionate AI developer. "
                "Always respond clearly and politely."
            )
        }
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.chat_history.append({"role": "user", "content": user_input})

    if any(keyword in user_input.lower() for keyword in CREATOR_KEYWORDS):
        reply = (
            "🤖 I'm IYNI!\n\n"
            "My creator is **Parthasarathi M** — a BSc CS with AI student "
            "and passionate future AI & web developer who loves building smart technology. 🚀"
        )
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        context = st.session_state.messages[-20:]

        with st.spinner("IYNI is thinking..."):
            try:
                chat_completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=context,
                    temperature=0.7,
                    max_tokens=512,
                )
                reply = chat_completion.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                reply = f"❌ Error: {e}"

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(reply)

    st.session_state.chat_history.append({"role": "assistant", "content": reply})
