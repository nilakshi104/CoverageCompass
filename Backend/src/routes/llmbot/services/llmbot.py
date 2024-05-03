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
        You are a seasoned AI car insurance agent tasked with assessing whether car damage is eligible for a claim under a given policy. 
        Your role involves thoroughly understanding the policy terms and correlating them with real-life situations. 
        Use your knowledge to interpret the policy comprehensively beyond its literal text.  \n\n
        Here are examples illustrating the integration of general knowledge and policy details in assessing claim eligibility:\n
        1) In scenarios of car theft, even though if the policy doesn't specifically mention about filing an FIR, 
        as it is a necessary step needed in this case, you should reject the claim if there is no FIR. \n
        2) If date of accident is in future compared to validation date of policy then you should reject the claim. \n\n
        Follow below steps to determine if car damage is claimable under provided policy :
	    1) Below policy text is provided as context. Using the provided policy context, 
        identify all necessary user inputs required to check claim eligibility. 
        Construct an algebraic expression incorporating these user input requirements using logical operators and variables. 
        Prompt the user to provide all necessary inputs in JSON format only. \n
        If you don't know the answer, just say that you don't know the answer. Do not try to make up an answer. \n
        Please do your best, my career depends on this. \n\n
        Context: """ + policy_data

        model= self.get_model()
        response = model.generate_content(query)
        # print("response under llmbot", response)
        return self.return_bot_response(response)
        
        
    
    def check_claim(self, policy, previous_result, user_data):
        query = """
        2) Below user data is provided as context. Incorporate below user data values into the algebraic expression generated in the previous step as given below. 
        Determine whether the damage is deemed "CLAIMABLE" or "NON-CLAIMABLE" based on the output of the algebraic expression.
        In both scenarios, briefly outline the factors influencing your decision-making process \n
        If you don't know the answer, just say that you don't know the answer. Do not try to make up an answer. \n
        Please do your best, my career depends on this. \n\n
        User data""" + user_data + "\n\n output from Prvious Step :" + previous_result + "\n\n policy details: " + policy

        model= self.get_model()
        response = model.generate_content(query)
        # return response.text
        return self.return_bot_response(response)
    
    


        



    


   

