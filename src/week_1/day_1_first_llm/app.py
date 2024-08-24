from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback
from simple import *

app = FastAPI()

@app.get('/healthz')
async def health():
    return {
        "application": "Simple LLM API",
        "message": "running succesfully"
    }


@app.post('/chat')
async def generate_chat(request: Request):

    query = await request.json()
    model = query["model"]
    
    try:
        temperature = float(query["temperature"])
    except:
        return {
            "error": "Invalid input, pass a number between 0 and 2."
        }

    if model not in models:
        return {
            "error": "You did not pass a correct model code!"
        }

    try:
        response = generate(
            model, 
            query["question"], 
            temperature=temperature
        )

        return {
            "status": "success",
            "response": response
        }
    
    except Exception as e:
        print(traceback.format_exc())
        return {
            "error": str(e),
            "status_code": 400
        }


if __name__ == "__main__":
    import uvicorn
    print("Starting LLM API")
    uvicorn.run(app, host="0.0.0.0", reload=True)

