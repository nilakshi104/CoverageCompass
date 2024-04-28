from flask import Flask,request
from flask_restx import Resource
from ...routes.bp import api
from .services import LLMBOT

@api.route("/gemini/chat")
class ChatBot(Resource):
    def post(self):
        try:
            request_data=request.get_json()
            query=request_data["query"]
            answer= LLMBOT().output_chat_response(query)
        except Exception as e:
            raise Exception(e)
        return answer, 200
    
    def get(self):
        print("Hello World")

@api.route("/gemini/userdata")
class ReqUserData(Resource):
    def post(self):
        try:
            request_data=request.get_json()
            policy=request_data["policy"]
            required_user_data= LLMBOT().ask_user_data(policy)
        except Exception as e:
            raise Exception(e)
        return required_user_data, 200

@api.route("/gemini/claimval")   
class ClaimVal(Resource):
    def post(self):
        try:
            request_data=request.get_json()
            policy, user_data=request_data["policy"], request_data["user_data"]
            claim_info = LLMBOT().check_claim(policy, user_data)
        except Exception as e:
            raise Exception(e)
        return claim_info, 200
    