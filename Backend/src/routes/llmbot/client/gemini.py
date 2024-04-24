import os
import google.generativeai as gen_ai
from dotenv import load_dotenv

class Client:
    def gemini_client():
        load_dotenv()
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        gen_ai.configure(api_key=GOOGLE_API_KEY)
        return gen_ai
