import os
import groq
from pydantic import BaseModel
from dotenv import load_dotenv
import traceback
load_dotenv()



class chat_bot():
    # Set GRO_API_KEY = "your api key" in the .env file, then load it below
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    
    # Run generative search otherwise
    client = groq.Groq(api_key=GROQ_API_KEY)
    query:str
    output:str = ""
    models = [
    # "llama-3.1-405b-reasoning",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768"
]
    output_type = ["Stream", "Batch"]
    token_class = { "short":150, "Moderate":700, "Long": 1536}
    sys_prompt = f"""You are an intelligent generative search assistant. As an expert in trained on diverse knowledge base, \
                        provide to the best of your ability response to my query using the most recent information"""
                        
    def get_response(self, message, token, model="llama-3.1-70b-versatile", temperature=0):
        try:            
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"{self.sys_prompt}"},
                    {"role": "user", "content": f"{message}"}
                ],
                stream=True,
                temperature=temperature,
                max_tokens= token,
            )
            return response
    
        except Exception as e:
            print(traceback.format_exc())
            return {
                "error": str(e),
                "status_code": 400
            }


    def get_response_batch(self, message, token, model="llama-3.1-70b-versatile", temperature=0):
        try:
            response = self.client.chat.completions.create(
                model = model,
                messages = [
                    {"role": "system", "content": f"{self.sys_prompt}"},
                    {"role": "user", "content": message},
                ],
                response_format = {"type": "text"},
                temperature = temperature,
                max_tokens=token
            )
            return response
    
        except Exception as e:
            print(traceback.format_exc())
            return {
                "error": str(e),
                "status_code": 400
            }
        
        