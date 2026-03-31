import streamlit as st
import requests

# =========================
# CONFIG
# =========================
API_URL = "http://127.0.0.1:8000/query"
MAX_HISTORY = 6   # last N messages sent to LLM

st.set_page_config(page_title="RAG Chat")

st.title("💬 Simple RAG Chatbot")

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# DISPLAY CHAT
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# INPUT
# =========================
user_input = st.chat_input("Ask something...")

if user_input:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # =========================
    # ✅ CLEAN HISTORY (FIX)
    # =========================
    history = [
        {
            "role": msg.get("role", ""),
            "content": msg.get("content", "")
        }
        for msg in st.session_state.messages[-MAX_HISTORY:]
    ]

    # =========================
    # API CALL
    # =========================
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                response = requests.post(
                    API_URL,
                    json={
                        "query": user_input,
                        "history": history
                    },
                    timeout=60
                )

                # ✅ HANDLE BACKEND ERRORS
                if response.status_code != 200:
                    st.error(f"Backend Error: {response.text}")
                    answer = "Something went wrong"
                else:
                    data = response.json()
                    answer = data.get("answer", "No response")

            except Exception as e:
                answer = f"Error: {str(e)}"

            st.markdown(answer)

    # Add assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })