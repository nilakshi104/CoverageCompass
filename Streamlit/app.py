import streamlit as st
import requests
from PyPDF2 import PdfReader
import json

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

def is_json(input_string):
    try:
        json_object = json.loads(input_string)
    except ValueError as e:
        return False
    return True

def return_assistant_response(response):
        try:
            if response.status_code == 200:
                # print("inside streamlit:",required_user_data.json())
                response = response.json()
                st.session_state.chat_history.append({"role": "assistant", "text": response})
                st.chat_message("assistant").markdown(response)
            else:
                st.error("Status_code", response.status_code)
        except Exception as e:
            st.error(f"An unexpected error occurred: {e} with Status_code {response.status_code}")

def main():
    st.set_page_config(page_title="Chat with Gemini-Powered CoverageCompass!",page_icon=":brain:",layout="centered")
    st.title("🤖 CoverageCompass") 

    if "chat_history" not in st.session_state:
        st.session_state.chat_history =[]

    for message in st.session_state.chat_history:
        with st.chat_message(translate_role_for_streamlit(message["role"])):
            st.markdown(message["text"])

    user_prompt = st.chat_input("Enter input to chat with CoverageCompass powered with gemini-1.5-pro-latest model")

    #Step1 : 
    with st.sidebar:
        st.markdown("""
        To determine if vehicle damage is eligible for a claim under the uploaded policy, adhere to the following instructions:
        1. Upload the policy document(s) and click "Submit & Proceed".
        2. The bot will prompt you to provide additional details about the incident in JSON format. Enter the details accordingly.
        3. The bot will assess the user's JSON response and the policy, then present the result as either "CLAIMABLE" or "NON-CLAIMABLE," along with reasoning. \n
        Happy botting!
        """)

        st.markdown("-"*30)

        uploaded_pdfs = st.file_uploader(label="Upload the policy documents below", type="pdf", accept_multiple_files=True)
        extracted_text = extract_text_from_pdf(uploaded_pdfs)
        submit_policy_pdf=st.button("Submit & Process")
    if submit_policy_pdf:
        with st.spinner("Processing..."):   
            required_user_data = requests.post('https://test-streamlit-app-1.onrender.com/covcomp/gemini/userdata', json={"policy":extracted_text})
            return_assistant_response(required_user_data)

    #Step2 :
    if user_prompt:
            if is_json(user_prompt):
                user_prompt= f"```json {user_prompt} ```"
            st.session_state.chat_history.append({"role": "user", "text": user_prompt})
            st.chat_message("user").markdown(user_prompt)
            with st.spinner("Processing..."):  
                claim_info = requests.post('https://test-streamlit-app-1.onrender.com/covcomp/gemini/claimval', json={"policy":extracted_text, "user_data":user_prompt})
                return_assistant_response(claim_info)


if __name__ == "__main__":
    main()