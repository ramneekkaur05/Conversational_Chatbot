import streamlit as st 
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# Streaming function
def stream_gemini(user_input):
    # Add user input to history
    st.session_state.history.append({"role": "user", "parts": [user_input]})

    # Pass full history to Gemini
    response_stream = model.generate_content(
        st.session_state.history,
        stream=True
    )

    full_text = ""
    for chunk in response_stream:
        if chunk.candidates and chunk.candidates[0].content.parts:
            token = chunk.candidates[0].content.parts[0].text
            full_text += token
            yield full_text

    # Save assistant response into history
    st.session_state.history.append({"role": "model", "parts": [full_text]})


def main():
    st.set_page_config(page_title='Conversational Chatbot', layout="centered")
    st.markdown(
        "<h1 style='text-align: center; color: white;'>CHATBOT 🤖</h1>",
        unsafe_allow_html=True
    )

    # Initialize history
    if "history" not in st.session_state:
        st.session_state.history = [
            {"role": "model", "parts": ["Hello, I am a conversational chatbot. You can ask me any question and I will answer you."]}
        ]

    for msg in st.session_state.history:
        display_role = "assistant" if msg["role"] == "model" else "user"
        with st.chat_message(display_role):
            st.markdown(msg["parts"][0])

    # Chat input
    if prompt := st.chat_input("Enter your query..."):
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("Just a second...")
            text = "" 
            for partial_text in stream_gemini(prompt):
                placeholder.markdown(partial_text)
                text = partial_text


if __name__ == "__main__":
    main()
