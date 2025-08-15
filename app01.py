from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_google_genai import GoogleGenerativeAI
import streamlit as st
import os
from dotenv import load_dotenv
import time

load_dotenv()

def chatbot(query, history):
    llm = GoogleGenerativeAI(
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        model="gemini-1.5-flash",
        temperature=0.6
    )
    memory = ConversationBufferMemory()

    for message in history:
        if message['role'] == "user":
            memory.chat_memory.add_user_message(message['content'])
        else:
            memory.chat_memory.add_ai_message(message['content'])

    conversation = ConversationChain(llm=llm, memory=memory, verbose=True)
    response = conversation.predict(input=query)

    history.append({'role': 'assistant', 'content': response})
    return response, history

def main():
    st.set_page_config(page_title='chatbot', layout='centered')
    st.title("CHATBOT 🤖")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show intro message only at start
    if not st.session_state.messages:
        st.session_state.messages.append({
            'role': 'assistant',
            'content': 'Hello, I am a conversational chatbot. You can ask me any question and I will answer you.'
        })

    # Display existing messages
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Enter your query here..."):
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        with st.chat_message('user'):
            st.markdown(prompt)

        with st.chat_message('assistant'):
            response, st.session_state.messages = chatbot(prompt, st.session_state.messages)
            st.markdown(response)  

if __name__ == "__main__":
    main()
