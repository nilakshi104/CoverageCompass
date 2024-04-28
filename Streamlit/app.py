import streamlit as st
import requests
from PyPDF2 import PdfReader

def extract_text_from_pdf(uploaded_pdfs):
    if uploaded_pdfs is not None:
        # pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
        text = ""
        # for page_num in range(pdf_reader.numPages):
        #     text += pdf_reader.getPage(page_num).extractText()
        for pdf in uploaded_pdfs:
            pdf_reader= PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    else:
        return None

def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

def main():
    st.set_page_config(page_title="Chat with Gemini-Powered CoverageCompass!",page_icon=":brain:",layout="centered")
    st.title("🤖 CoverageCompass") 

    if "chat_history" not in st.session_state:
        st.session_state.chat_history =[]

    for message in st.session_state.chat_history:
        with st.chat_message(translate_role_for_streamlit(message["role"])):
            st.markdown(message["text"])

    #Step1 : 
    uploaded_pdfs = st.file_uploader("Upload your Policy PDFs to know required user data to be fed", type="pdf", accept_multiple_files=True)
    extracted_text = extract_text_from_pdf(uploaded_pdfs)
    required_user_data = requests.post('https://test-streamlit-app-1.onrender.com/covcomp/gemini/userdata', json={"policy":extracted_text})
    if required_user_data.status_code == 200:
        # required_user_text = required_user_data.json()
        st.session_state.chat_history.append({"role": "assistant", "text": required_user_data.json()})
        st.chat_message("assistant").markdown(required_user_data.json())
    else:
        st.error(f"Error: {required_user_data.status_code}")

    #Step2 :
    user_prompt = st.chat_input("Enter required user data in JSON formate")
    st.session_state.chat_history.append({"role": "user", "text": user_prompt})
    claim_info = requests.post('https://test-streamlit-app-1.onrender.com/covcomp/gemini/claimval', json={"policy":extracted_text, "user_data":user_prompt})
    if claim_info.status_code == 200:
        claim_info_text = claim_info.json()
        st.session_state.chat_history.append({"role": "assistant", "text": claim_info_text})
        st.chat_message("assistant").markdown(claim_info_text)
    else:
        st.error(f"Error: {claim_info.status_code}")


if __name__ == "__main__":
    main()

    # if user_prompt:
    #     st.session_state.chat_history.append({"role": "user", "text": user_prompt})
    #     st.chat_message("user").markdown(user_prompt)
    #     gemini_response = requests.post('https://test-streamlit-app-1.onrender.com/claimval/gemini/chat', json={"query":user_prompt})
    #     if gemini_response.status_code == 200:
    #         gemini_text = gemini_response.json()
    #         st.session_state.chat_history.append({"role": "assistant", "text": gemini_text})
    #         st.chat_message("assistant").markdown(gemini_text)
    #     else:
    #         st.error(f"Error: {gemini_response.status_code}")


# def main():
#     st.set_page_config("Chat PDF")
#     st.header("Chat with PDF using Gemini💁")

#     user_question = st.text_input("Ask a Question from the PDF Files")

#     if user_question:
#         user_input(user_question)

#     with st.sidebar:
#         st.title("Menu:")
#         pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
#         if st.button("Submit & Process"):
#             with st.spinner("Processing..."):
#                 raw_text = get_pdf_text(pdf_docs)
#                 text_chunks = get_text_chunks(raw_text)
#                 get_vector_store(text_chunks)
#                 st.success("Done")

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
