import streamlit as st
import requests

st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",
    layout="centered"
)

st.title("🤖 Gemini Pro - ChatBot")


user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # response = requests.get('http://127.0.0.1:5000/claimval/gemini/chat')
    st.write(user_prompt)
    response = requests.post('http://127.0.0.1:5000/claimval/gemini/chat', json={"query":user_prompt})
    if response.status_code == 200:
        data = response.json()
        st.write(data)
    else:
        st.error(f"Error: {response.status_code}")






# def translate_role_for_streamlit(user_role):
#     if user_role == "model":
#         return "assistant"
#     else:
#         return user_role

# Initialize chat session in streamlit if not already present
# if "chat_session" not in st.session_state:
#     st.session_state.chat_session = LLMBOT().generate_response().start_chat(history=[])

# for message in st.session_state.chat_session.history:
#     with st.chat_message(translate_role_for_streamlit(message.role)):
#         st.markdown(message.parts[0].text)

# Input field for user's message

# if user_prompt:
#     response = 
    # Add user's message to chat and display it
    # st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    # gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # # Display Gemini-Pro's response
    # with st.chat_message("assistant"):
    #     st.markdown(gemini_response.text)
