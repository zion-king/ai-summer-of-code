## Simple FastAPI for Q&A LLM System

To run app.py, run the following command in your terminal:

`uvicorn app:app --host 127.0.0.1 --port 5000 --reload`

You can update the host and port number to any other values you choose

Request body for testing in Postman

```
    {
        "question": "which is bigger? 9.11 or 9.9?",
        "model": "llama-3.1-8b-instant",
        "temperature": 0.2
    }
```

