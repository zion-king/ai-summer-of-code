# Load .env file using:
from dotenv import load_dotenv
load_dotenv()
import os

Env= os.getenv("PYTHON_ENV")
app_port = os.getenv("PORT")
groq_key = os.getenv("groq_key")
auth_user = os.getenv("AUTH_USERNAME")
auth_password = os.getenv("AUTH_PASSWORD")
mongo_host =os.getenv("DB_HOST")
mongo_port= os.getenv("DB_PORT")
mongo_user= os.getenv("DB_USER")
mongo_password= os.getenv("DB_PASSWORD")
