import streamlit as st
from google import genai

st.title("Gemini Chatbot")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Build conversation history
    history = ""
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        history += f"{role}: {msg['content']}\n"

    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=history,
        )

        st.markdown(response.text)

    st.session_state.messages.append(
        {"role": "assistant", "content": response.text}
    )
