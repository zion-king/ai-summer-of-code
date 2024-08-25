# Mid-Camp Project: RAG System for a Targeted Use Case

## 1. Objective
Develop a practical use case for conversation-based information retrieval relevant to a specific niche or industry. Based on this use case, implement a simple RAG chatbot that takes in document(s) via file upload, generates embeddings of the documents, stores the embeddings in a vector store (e.g., Chroma), and retrieves relevant embeddings to answer the user's query. 

## 2. Implementation
Try to stick with the frameworks we have used so far during our sessions (FastAPI, LlamaIndex or Langchain or AdalFlow, MongoDB or ChromaDB, Streamlit). You are allowed to play around with other frameworks as long as you provide descriptions or explanations of how others can run your code to reproduce your results.

### Models
Your app should utilise the following 5 models or 7 only if you have an OpenAI API key:
- Via Groq:
    - `llama-3.1-70b-versatile`
- Via Vertex AI on GCP:
    - `gemini-1.5-pro-001`
    - `mistral-large@2407`
- Via AnthropicVertex (GCP):
    - `claude-3-opus@20240229`
    - `claude-3-5-sonnet@20240620`
- OpenAI (optional):
    - `gpt-4o`
    - `gpt-4o-mini`

For Vertex and AnthropicVertex models, refer to the tutorial on how to enable the models, create Vertex AI credentials on GCP and use the credentials to instantiate the Vertex API service for accessing these models. For covenience and modularity, you can create a `models.py` script in your codebase and define a class with methods implemented for each of the models.


### Model Runs
Two options - you can experiment with both and decide which version you want to submit.
- Dropdown for user selection of models at request level (one model run at a time)
- Dropdown for user selection of models at response level (all models return response in parallel, and a user can switch to see each response). We will particularly like to see how you go about multithreading or parallel execution in this step.

### Chat History
Implement conversation history using either of LlamaIndex's or Langchain's memory buffer implementation. You can implement in-session storage for your chat history using these implementations and ensure to reset chat history when necessary. Remember, this project is not intended to be a production-grade application, so you shouldn't worry about having different users chatting in different sessions.

### Logging & Exception Handling
Ensure you catch and manage exceptions effectively. Implement logging in your codebase replicating what we covered in Week 3 Day 1 and feel free to make your own logging customizations. **Please don't push your log files to the project repo. Add a .gitignore in your codebase to untrack your .log files.**


## 3. Experimentation & Evaluation
### Prompt Engineering
Experiment with different system prompts until you find a robust prompt that works well. AdalFlow can come in handy here so you don't expend too much manual effort crafting an effective prompt. 

### Retrieval
Experiment with different *k* values to determine the optimal _k_ value for your use case and for different document sizes (small, medium and large). 

### Evaluation
Evaluate different components of your application using both manual and tool-based evaluation. For retrieval and model performance, evaluate things like retrieval acccuracy, generation accuracy, etc. Use this to understand which models work well for specific tasks and which ones work well across board. This part is very open-ended so we welcome your creativity, but also don't ovrthink it.

**Implement logging for your evaluation:** Create custom logging for evaluation in your `operationshandler` script and add a file named `evals.log` to log all your evaluation results. **This part is crucial as you will be submitting your **evals.log** file along with your project for review.**


## 4. Deployment
Deploy your streamlit application to Streamlit cloud to expose your application via HTTPs so you can share with others. To do this, you will need to follow these steps:

- Create a github repository specifically for your project or application
- Navigate to [Streamlit Community Cloud](https://streamlit.io/cloud), click the `New app` button, and choose the appropriate repository, branch, and application file.
- Finally, hit the `Deploy` button. Your app will be live in seconds!


## 5. Submission

### Documentation
- Decsribe your use case in a `readme.md` file at the root of your project repository.
- Provide a description of the tech stack you have used for your project, and how your solution can be improved or any future work.
- Provide a brief technical walkthrough of your codebase/application and how other developers can run your code locally to reproduce your results.
- Optionally, add the URL of your deployed streamlit application to the `About` section of your project repository.

### Submission Items
- Project Name
- Project Description
- Project Repo URL
- Evals log file
- Project Demo Video (Optional)
- Streamlit or Frontend App

### Submission Deadline
There's no strict submission deadline. However, if you submit before **August 31st**, we will be able to review early and give you feedback. Remember, there's going to be a second project which will be the Capstone.

When you are ready, [submit your project here](https://github.com/zion-king/ai-summer-of-code/issues/new?assignees=&labels=&projects=&template=project.yml&title=Project%3A+%3Cshort+description%3E)


# Capstone Project: TBA

