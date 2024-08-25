# Project 1: RAG System for Targeted Use Cases

## Objective
Develop a practical use case for conversation-based information retrieval relevant to a specific niche or industry. Based on this use case, implement a simple RAG chatbot that takes in document(s) via file upload, generates embeddings of the documents, stores the embeddings in a vector store (e.g., Chroma), and retrieves relevant embeddings to answer the user's query. 

## Implementation
Try to stick with the frameworks we have used so far during our sessions (FastAPI, LlamaIndex or Langchain, MongoDB or ChromaDB, Streamlit). You are allowed to play around with other frameworks as long as you provide descriptions or explanations of how others can run your code to reproduce your results.

### Models
Your app should utilise the following 7 models:
- Via Groq:
    - `llama-3.1-70b-versatile`
    - `mixtral-8x7b-32768`
- Via Vertex AI on GCP:
    - `gemini-1.5-flash-001`
    - `gemini-1.5-pro-001`
    - `mistral-large@2407`
- Via AnthropicVertex (GCP):
    - `claude-3-opus@20240229`
    - `claude-3-5-sonnet@20240620`

For covenience, you can create a `models.py` script in your codebase and define a class with methods implemented for each of the models.

### Model Runs
Two options - you can play with both and decide which version you want to submit
- Dropdown for user selection of models at request level (one model run at a time)
- Dropdown for user selection of models at response level (all models return response in parallel, and users can switch to see response)

### Logging
Implement custom logging in your codebase replicating what we covered in Week 3 Day 1 or feel free to make your own logging customizations.


## Submission

### Documentation
- Decsribe your use case in a `readme.md` file at the root of your project repository.
- In the `readme.md` file, provide a brief technical walkthrough of your codebase/application and how other developers can run your code to reproduce your results

### Submission Items
- Project Name
- Project Description
- Project Repo URL
- Project Demo Video (Optional)
- Streamlit or Frontend App


# Project 2: TBA

