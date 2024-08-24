import traceback
from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
from src.week_3.day_1_swe_logging.simple import *
from src.exceptions.operationshandler import userops_logger, llmresponse_logger

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

    userops_logger.info(
        f"""
        User Request: 
        -----log prompt-----
        User data: {query}
        """
    )

    model = query["model"]
    
    try:
        temperature = float(query["temperature"])
    except:
        return {
            "status_code": 400,
            "error": "Invalid input, pass a number between 0 and 2."
        }
    
    if model == "llama-3.1-405b-reasoning":
        return {
            "status_code": 403,
            "error": "You do not yet hava access to this model. Please try a different model instead."
        }

    elif model not in models:
        return {
            "status_code": 404,
            "error": "You did not pass a correct model code!"
        }

    response = generate(
        model, 
        query["question"], 
        temperature=temperature
    )

    if response == None: # i.e., exception caught in simple.py generate() and nothing was returned
        return {
            "status_code": 500,
            "response": response
        }

    else:
        llmresponse_logger.info(
            f"""
            LLM Response: 
            -----log response-----
            Response: {response}
            """
        )

        return {
            "status_code": 200,
            "response": response
        }


if __name__ == "__main__":
    import uvicorn
    print("Starting LLM API")
    uvicorn.run(app, host="0.0.0.0", reload=True)



