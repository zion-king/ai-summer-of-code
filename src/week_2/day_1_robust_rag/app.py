import tempfile, traceback, asyncio
from typing import List, Literal, Any
from fastapi import FastAPI, Request, UploadFile, Depends
from fastapi.responses import PlainTextResponse
from src.week_2.day_1_robust_rag.main import *
from src.week_2.day_1_robust_rag.utils.helpers import *
from src.week_2.day_1_robust_rag.utils.models import LLMClient
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()


class EmbeddingState:
    """
    Implementation of dependency injection intended for working locally with \
        embeddings via in-session storage. It allows you to have session-wide access \
            to embeddings across the different endpoints. \
                This is not ideal for production.
    """

    def __init__(self):
        self.embedding = None

    def get_embdding_state():
        return state

state = EmbeddingState()


@app.get('/healthz')
async def health():
    return {
        "application": "Simple LLM API",
        "message": "running succesfully"
    }

@app.post('/upload')
async def process(
    files: List[UploadFile] = None,
    # urls: List[str] = None,
    state: EmbeddingState = Depends(EmbeddingState.get_embdding_state)
):

    try:
        with tempfile.TemporaryDirectory() as temp_dir:

            _uploaded = await upload_files(files, temp_dir)

            if _uploaded["status_code"]==200:
                documents = SimpleDirectoryReader(temp_dir).load_data()
                state.embedding = VectorStoreIndex.from_documents(documents)
                        
                return {
                    "detail": "Embeddings generated succesfully",
                    "status_code": 200
                }
            else:
                return _uploaded # returns status dict

    except Exception as e:
        print(traceback.format_exc())
        return {
            "detail": f"Could not generate embeddings: {e}",
            "status_code": 500
        }


@app.post('/generate')
async def generate_chat(
    request: Request,
    state: EmbeddingState = Depends(EmbeddingState.get_embdding_state)
):

    query = await request.json()
    model = query["model"]
    temperature = query["temperature"]

    init_client = LLMClient(
        groq_api_key = GROQ_API_KEY, 
        secrets_path="./service_account.json",
        temperature=temperature
    )
    
    llm_client = init_client.map_client_to_model(model)

    try:
        response = qa_engine(
            query["question"], 
            state.embedding,
            llm_client, 
            # model=model
        )

        print(response.response)
        return PlainTextResponse(content=response.response, status_code=200)
    
    except Exception as e:
        message = f"An error occured where {model} was trying to generate a response: {e}",
        system_logger.error(
            message,
            exc_info=1
        )
        raise QueryEngineError(message)


if __name__ == "__main__":
    import uvicorn
    print("Starting LLM API")
    uvicorn.run(app, host="0.0.0.0", reload=True)

