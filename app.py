import streamlit as st 
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def stream_gemini(prompt):
    response_stream = model.generate_content(prompt, stream=True)
    full_text = ""
    for chunk in response_stream:
        if chunk.candidates and chunk.candidates[0].content.parts:
            token = chunk.candidates[0].content.parts[0].text
            full_text +=token
            yield full_text

def main():
    st.set_page_config(page_title='Conversational Chatbot',layout="centered")
    st.markdown(
    "<h1 style='text-align: center; color: white;'>CHATBOT 🤖</h1>",
    unsafe_allow_html=True
    )

    if "history" not in st.session_state:
        st.session_state.history = []

    if not st.session_state.history:
        st.session_state.history.append(("assistant","Hello, I am a conversational chatbot. You can ask me any question and I will answer you."))

    for role, content in st.session_state.history:
        with st.chat_message(role):
            st.markdown(content)
    
    if prompt := st.chat_input("Enter you query..."):
        st.session_state.history.append(("user",prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("Just a second...")
            text = "" 
            for partial_text in stream_gemini(prompt):
                placeholder.markdown(partial_text)
                text = partial_text
            st.session_state.history.append(('assistant',text))

if __name__ =="__main__":
    main()