import os
import google.generativeai as gen_ai
from ..client import Client
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains.question_answering import load_qa_chain
# from langchain.prompts import PromptTemplate

class LLMBOT:
    def __init__(self):
        self.gemini_client = Client.gemini_client()

    def return_bot_response(self, response):
        try:
            # Check if 'candidates' list is not empty
            if response.candidates:
                # Access the first candidate's content if available
                if response.candidates[0].content.parts:
                    generated_text = response.candidates[0].content.parts[0].text
                    print("Generated Text:", generated_text)
                    return generated_text
                else:
                    print("No generated text found in the candidate.")
                    return "No generated text found in the candidate."
            else:
                print("No candidates found in the response.")
                return "No candidates found in the response."
        except (AttributeError, IndexError) as e:
            raise Exception("Error", e)

    def get_model(self):
        #set up model
        generation_config={
            "temperature":0.3,
            "top_p":1,
            "top_k":1,
            "max_output_tokens":400
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_DANGEROUS",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]
        model = self.gemini_client.GenerativeModel(model_name='gemini-1.5-pro-latest',
                                                    # generation_config=generation_config,
                                                    safety_settings=safety_settings)
        return model
    
    def output_chat_response(self, query):
        model= self.get_model()
        response = model.generate_content(query)
        return response.text
    
    def ask_user_data(self, policy_data):
        query = """
        Below policy text is provided as context. Understand the context and output necessary json inputs required from user to verify if their damage is claimable under the policy provided in context. Note that only json should be returned as answer.
        Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
        provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
        Context: """ + policy_data

        model= self.get_model()
        response = model.generate_content(query)
        # print("response under llmbot", response)
        return self.return_bot_response(response)
        
        
    
    def check_claim(self, policy_data, user_data):
        query = """
        Below policy text is provided as context. Use Context and User data json provided below and output if user can get claim on not. Output one liner. Output "Non claimable" if user can't claim policy and "Claimable" in other case
        Context: """ + policy_data + "\n\n User data" + user_data

        model= self.get_model()
        response = model.generate_content(query)
        # return response.text
        return self.return_bot_response(response)

    


# Below code is useful for implementing RAG
# model = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)
# prompt = PromptTemplate(template = prompt_template, input_variables = ["context"])
# chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
# response = chain({"context":policy_data}, return_only_outputs=True)
    
    
    


        



    


   

