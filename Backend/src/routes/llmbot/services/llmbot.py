import os
import google.generativeai as gen_ai
from ..client import Client
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains.question_answering import load_qa_chain
# from langchain.prompts import PromptTemplate

class LLMBOT:
    def __init__(self):
        self.gemini_client = Client.gemini_client()

    def get_model(self):
        model = self.gemini_client.GenerativeModel('gemini-1.5-pro-latest')
        return model
    
    def output_chat_response(self, query):
        model= self.get_model()
        response = model.generate_content(query)
        return response.text
    
    def ask_user_data(self, policy_data):
        query = """
        Below policy text is provided as context. Understand the context and output necessary inputs required from user to verify if their damage is claimable under the policy provided in context.
        Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
        provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
        Context: """ + policy_data

        model= self.get_model()
        response = model.generate_content(query)
        return response.text
    


# Below code is useful for implementing RAG
# model = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)
# prompt = PromptTemplate(template = prompt_template, input_variables = ["context"])
# chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
# response = chain({"context":policy_data}, return_only_outputs=True)
    
    
    


        



    


   

