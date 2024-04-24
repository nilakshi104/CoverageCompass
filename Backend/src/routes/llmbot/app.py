from flask import Flask,request
from flask_restx import Resource
from ...routes.bp import api
from .services import LLMBOT

@api.route("/gemini/chat")
class ClaimVal(Resource):
    def post(self):
        try:
            request_data=request.get_json()
            query=request_data["query"]
            answer= LLMBOT().generate_response(query)
        except Exception as e:
            raise Exception(e)
        return answer, 200
    
    def get(self):
        print("Hello World")

    