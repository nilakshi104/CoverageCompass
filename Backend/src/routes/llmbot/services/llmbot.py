import os
import google.generativeai as gen_ai
from ..client import Client

class LLMBOT:
    def __init__(self):
        self.gemini_client = Client.gemini_client()

    def generate_response(self, query):
        model = self.gemini_client.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content(query)
        return response.text
    
    
    


        



    


   

