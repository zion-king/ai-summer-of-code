from airflow.decorators import dag, task
from datetime import datetime, timedelta
import os
import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

# Configuration
PDF_DIR = "/usr/local/airflow/data"  # Path to the directory with PDF files
CHROMA_PATH = "/usr/local/airflow/chromadb"  # ChromaDB Path
PROCESSED_FILES_LOG = "/usr/local/airflow/log/processed_files.log"  # Log file to track processed PDFs

# Initialize the OpenAI Embedding model
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Load OpenAI API Key from environment variable
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 28),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    default_args=default_args,
    schedule_interval=timedelta(minutes=5),
    catchup=False,
    description='A DAG to ingest, split, and embed new PDFs into ChromaDB every 5 minutes',
)
def pdf_ingestion_and_embedding():
    
    @task
    def check_for_new_pdfs():
        # Load the list of already processed files
        if os.path.exists(PROCESSED_FILES_LOG):
            with open(PROCESSED_FILES_LOG, 'r') as f:
                processed_files = f.read().splitlines()
        else:
            processed_files = []

        # Identify new PDFs
        new_pdfs = [f for f in os.listdir(PDF_DIR) if f.endswith('.pdf') and f not in processed_files]

        if new_pdfs:
            logging.info(f"New PDFs found: {new_pdfs}")
            return new_pdfs
        else:
            logging.info("No new PDFs found")
            return []

    @task
    def process_pdfs(new_pdfs):
        if not new_pdfs:
            logging.info("No new PDFs to process")
            return

        all_chunks = []

        # Loop through new PDFs and process them
        for pdf_file in new_pdfs:
            file_path = os.path.join(PDF_DIR, pdf_file)
            loader = PyPDFLoader(file_path)
            pages = loader.load()

            # Split the document into smaller chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = text_splitter.split_documents(pages)

            all_chunks.extend(chunks)

        # Embed the chunks and load them into the ChromaDB
        db_chroma = Chroma.from_documents(all_chunks, embeddings, persist_directory=CHROMA_PATH)

        # Persist the database
        db_chroma.persist()
        
        logging.info(f"Chroma DB persisted at {CHROMA_PATH}")
        # Update the processed files log
        with open(PROCESSED_FILES_LOG, 'a') as f:
            for pdf_file in new_pdfs:
                f.write(pdf_file + "\n")

    # Task dependencies
    new_pdfs = check_for_new_pdfs()
    process_pdfs(new_pdfs)

dag = pdf_ingestion_and_embedding()
