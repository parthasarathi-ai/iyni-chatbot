import streamlit as st
from groq import Groq

# ⚠️ Replace with your NEW api key from console.groq.com
api_key = "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"

client = Groq(api_key=api_key)

CREATOR_KEYWORDS = ["created you", "made you", "creator", "founder", "developer", "built you", "invented you", "who are you made by"]

# Page config
st.set_page_config(
    page_title="IYNI AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Header
st.title("🤖 IYNI AI Chatbot")
st.caption("Created by Parthasarathi M — BSc CS with AI Student")
st.divider()

# Initialize memory
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": (
            "You are IYNI, a smart and friendly AI chatbot created by Parthasarathi M, "
            "a BSc Computer Science with Artificial Intelligence student and passionate AI developer. "
            "Be helpful, concise, and friendly in all responses."
        )
    }]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Generate response
    if any(kw in user_input.lower() for kw in CREATOR_KEYWORDS):
        reply = "I'm IYNI! My creator is **Parthasarathi M** — a BSc CS with AI student and passionate future AI & web developer who loves building smart technology. 🚀"
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        context = [st.session_state.messages[0]] + st.session_state.messages[-20:]

        with st.spinner("IYNI is thinking..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=context,
                    model="llama-3.1-8b-instant",
                    temperature=0.7,
                    max_tokens=512,
                )
                reply = chat_completion.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                reply = f"Sorry, I encountered an error: {e}"

    # Show IYNI response
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(reply)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})