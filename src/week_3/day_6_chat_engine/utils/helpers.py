import os, chromadb
from pydantic import BaseModel
from werkzeug.utils import secure_filename
from src.exceptions.operationshandler import system_logger
from llama_index.llms.groq import Groq
from llama_index.core import (
    VectorStoreIndex, 
    SimpleDirectoryReader, 
    Settings, StorageContext, 
    load_index_from_storage
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.memory.chat_memory_buffer import ChatMemoryBuffer


allowed_files = ["txt", "csv", "json", "pdf", "doc", "docx", "pptx"]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_files


def file_checks(files):

    if not files:
        return {
            "detail": "No file found",
            "status_code": 400
        }

    for file in files:
        if not file or file.filename == '':
            return {
                "detail": "No selected file",
                "status_code": 400
            }
        
        if not allowed_file(file.filename):
            print(file.filename)
            return {
                "detail": f"File format not supported. Use any of {allowed_files}",
                "status_code": 415
            }
    
    return {
        "detail": "success",
        "status_code": 200
    }

async def upload_files(files, temp_dir):

    checks = file_checks(files)
    
    if checks["status_code"] == 200:
        try: 
            for file in files:
                filename = secure_filename(file.filename)
                file_path = os.path.join(temp_dir, filename)

                file_obj = await file.read()

                with open(file_path, "wb") as buffer:
                    buffer.write(file_obj)
                
            return {
                "detail": "Upload completed",
                "status_code": 200
            }
    
        except Exception as e:
            message = f"An error occured during upload: {e}"
            system_logger.error(
                message,
                # str(e),
                exc_info=1
            )
            raise UploadError(message)

    return checks


def init_chroma(collection_name, path="C:/Users/HP/chroma_db"):
    db = chromadb.PersistentClient(path=path)
    chroma_collection = db.get_or_create_collection(collection_name)
    return chroma_collection

def get_kb_size(collection):
    return collection.count()

def get_vector_store(chroma_collection):
    
    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    return vector_store


class UploadError(Exception):
    pass

class QueryEngineError(Exception):
    pass

class ChatEngineError(Exception):
    pass


SYSTEM_PROMPT_TEMPLATE = f"""
You are a helpful and intelligent conversational assistant. Your goal is to use the information provided below to answer my request.\
    This information has been extracted from a set of documents, and I will often make reference to the "document(s)" in my requests. \
        Do not hallucinate an answer - if the requested answer cannot be found in the provided information, just indicate so.
"""

class ChatEngine:
    
    def __init__(
        self, 
        chatbot_name:str = "",
        system_prompt:str = SYSTEM_PROMPT_TEMPLATE,
        chat_mode:str = "context",
        verbose:bool = True,
        streaming:bool = True,
    ):
        self.chatbot_name = chatbot_name
        self.system_prompt = system_prompt
        self.chat_mode=chat_mode
        self.verbose=verbose
        self.streaming=streaming

    def qa_engine(
        self, 
        query: str, 
        index: VectorStoreIndex, 
        llm_client,
        choice_k:int=5,
        memory=None,
    ):

        chatbot_desc = f"Your name is {self.chatbot_name}. " if self.chatbot_name else ""
        print(chatbot_desc)
        
        system_prompt = "".join([chatbot_desc, self.system_prompt])
        memory = memory or self.create_chat_memory(choice_k)

        chat_engine = index.as_chat_engine(
            llm=llm_client,
            chat_mode=self.chat_mode,
            system_prompt=system_prompt,
            similarity_top_k=choice_k,
            # token_limit=self.token_limit,
            memory=memory,
            verbose=self.verbose,
            streaming=self.streaming
            )
        
        try:
            response = chat_engine.stream_chat(query)
            print("Starting response stream...\n")

            for token in response.response_gen:
                print(token, end="")
                yield str(token)

        except Exception as e:
            message = f"An error occured while chat engine was generating response: {e}"
            system_logger.error(
                message,
                exc_info=1
            )
            raise ChatEngineError(message)

        
    def create_chat_memory(self, choice_k) -> ChatMemoryBuffer:
        """
        Convenience method for creating and using chat history within an app session. \
            Can be further customised for use in production"""
        
        token_limit=choice_k*1024+200 # set token_limit to accommodate all the input tokens from the choice-k chunks
        return ChatMemoryBuffer.from_defaults(token_limit=token_limit)
    
    def get_chat_memory(self, choice_k, app_state = None):
        """
        Convenience method for retrieving chat history within an app session. \
            Don't use this in production - store and load chat history from a db"""
        
        try:
            return app_state.chat_memory or self.create_chat_memory(choice_k)
        except:
            return self.create_chat_memory(choice_k)
    
    
    def get_conversation_history(self, db_client, chat_uuid, choice_k):    
    
        """
        Convenience method for loading chat history from a db and transforming it into a ChatMemoryBuffer object. \
            Suitable for production. Customise this to suit your need."""

        # create new memory instance if no chat ID provided
        if not chat_uuid:
            return self.create_chat_memory(choice_k)
        
        token_limit=choice_k*1024+200
        memory_instance = ChatMemoryBuffer(token_limit=token_limit)
        history = []

        print("Retrieving conversation history...")

        messages = db_client.get_chat_history(chat_uuid)

        _history = [
            item if message['response'] and message['query'] else None \
                for message in messages for item in (
                    [{'additional_kwargs': {}, 'content': message['response'], 'role': 'assistant'}]
                ) + 
                (
                    [{'additional_kwargs': {}, 'content': message['query'], 'role': 'user'}]
                )
            ]
        
        # reverse history and filter out None items
        history = list(filter(None, reversed(_history)))
        history = history[:5] if 5<len(history) else history # trim
        # Or create a history trimmer to trim the history length by the token limit
        # history = history_trimmer(history, token_limit)

        memory_dict = {'chat_history': history[:5], 'token_limit': token_limit}
        return memory_instance.from_dict(memory_dict)
