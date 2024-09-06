import os, tempfile, traceback
from typing import List, Literal, Any
from fastapi import FastAPI, Request, Form, UploadFile, Depends
from fastapi.responses import PlainTextResponse, StreamingResponse
from src.week_3.day_6_chat_engine.utils.helpers import *
from src.week_3.day_6_chat_engine.utils.models import LLMClient
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHROMADB_PATH = "../../chroma_db" # for prototyping only - NOT suitable for production
CREDENTIALS_PATH = "./service_account.json"

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

app = FastAPI()
app.state.chat_memory = None # for prototyping only - don't use this in production

@app.get('/healthz')
async def health():
    return {
        "application": "Simple LLM API",
        "message": "running succesfully"
    }

@app.post('/upload')
async def process(
    projectUuid: str = Form(...),
    files: List[UploadFile] = None,
):

    try:
        with tempfile.TemporaryDirectory() as temp_dir:

            _uploaded = await upload_files(files, temp_dir)

            if _uploaded["status_code"]==200:

                documents = SimpleDirectoryReader(temp_dir).load_data()

                collection_name = projectUuid
                chroma_collection = init_chroma(collection_name, path=CHROMADB_PATH)

                print(f"Existing collection size::: {get_kb_size(chroma_collection)}...")

                vector_store = get_vector_store(chroma_collection)
                storage_context = StorageContext.from_defaults(vector_store=vector_store)
                
                embedding = VectorStoreIndex.from_documents(
                    documents, storage_context=storage_context
                )

                print(f"Collection size after new embedding::: {get_kb_size(chroma_collection)}...")
                        
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
):

    query = await request.json()
    model = query["model"]
    temperature = query["temperature"]

    init_client = LLMClient(
        groq_api_key = GROQ_API_KEY, 
        secrets_path=CREDENTIALS_PATH,
        temperature=temperature,
        max_output_tokens=1024
    )
    
    llm_client = init_client.map_client_to_model(model)
    
    chroma_collection = init_chroma(query['projectUuid'], path=CHROMADB_PATH)
    collection_size = get_kb_size(chroma_collection)
    print(f"\n\nCollection size::: {collection_size}...")

    vector_store = get_vector_store(chroma_collection)
    doc_embeddings = VectorStoreIndex.from_vector_store(
        vector_store=vector_store
    )

    # experiment with choice_k to find something optimal
    choice_k = 20 if collection_size>150 \
                    else 10 if collection_size>50 \
                        else 5
    
    print(f"Retrieving top {choice_k} chunks from the knowledge base...")

    # For prototyping only, to persist chat history in the app sesion
    # Don't use this approach in production, store and load chat history from a db instead
    app.state.chat_memory = ChatEngine().get_chat_memory(choice_k, app_state=app.state)
    chat_history = app.state.chat_memory

    response = ChatEngine().qa_engine(
        query["question"], 
        doc_embeddings,
        llm_client,
        choice_k=choice_k,
        memory=chat_history
    )

    return StreamingResponse(content=response, status_code=200)
    # return StreamingResponse(content=response, status_code=200, media_type="text/event-stream") # use this option for production


if __name__ == "__main__":
    import uvicorn
    print("Starting LLM API")
    uvicorn.run(app, host="0.0.0.0", reload=True)

