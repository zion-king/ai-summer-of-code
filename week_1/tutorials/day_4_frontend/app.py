# import os
# import groq
from model import ChatBot
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, PlainTextResponse
from dotenv import load_dotenv
import traceback

load_dotenv()

# initialise app
app = FastAPI()
chatbot = ChatBot()

client = chatbot.client

@app.route("/chat_batch", methods=["POST"])
async def chat_batch(request: Request):
    user_input = await request.json()
    user_message = user_input.get("message")
    temperature = float(user_input.get("temperature"))
    selected_model  = user_input.get("model")
    
    try:
        # Generate a response
        response = chatbot.get_response_batch(message=user_message, temperature=temperature, model=selected_model)
        output = response.choices[0].message.content
        return PlainTextResponse(content=output, status_code=200)
    
    except Exception as e:
        print(traceback.format_exc())
        return {
            "error": str(e),
            "status_code": 400
        }



