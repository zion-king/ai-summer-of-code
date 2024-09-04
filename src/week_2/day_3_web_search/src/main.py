# Import required modules
import asyncio, gc, secrets, uvicorn, re
from src.api_models.chat_model import ChatRequest
from src.agent.llm import LLM_Model
from src.agent.toolkit.base import AISoCTools
from src.inference import StreamConversation
from contextlib import asynccontextmanager
from fastapi import FastAPI, status, HTTPException, Depends
from src.config.settings import get_setting
from fastapi.middleware.cors import CORSMiddleware
from src.config import appconfig
from fastapi.responses import JSONResponse
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from src.utilities.Printer import printer
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# Get application settings
settings = get_setting()

# Description for API documentation
description = f"""
{settings.API_STR} helps you do awesome stuff. 🚀
"""

# Garbage collect to free up resources
gc.collect()

# Instantiate basicAuth
security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    """
    This function sets up the basic auth url protection and returns the credential name.

    Args:
        credentials (HTTPBasicCredentials): Basic auth credentials.

    Raises:
        HTTPException: If the username or password is incorrect.

    Returns:
        str: The username from the credentials.
    """
    correct_username = secrets.compare_digest(credentials.username, appconfig.auth_user)
    correct_password = secrets.compare_digest(
        credentials.password, appconfig.auth_password
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect userid or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

api_llm = LLM_Model()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for application lifespan.
    This function initializes and cleans up resources during the application's lifecycle.
    """
    print(running_mode)
    # MongoDB configuration
    # MongoDBContextConfig()
    print()
    AISoCTools()
    print()
    printer(" ⚡️🚀 AI Server::Started", "sky_blue")
    print()
    printer(" ⚡️🏎  AI Server::Running", "sky_blue")
    yield
    printer(" ⚡️🚀 AI Server::SHUTDOWN", "red")


# Create FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    openapi_url=f"{settings.API_STR}/openapi.json",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    lifespan=lifespan,
)

# Configure for development or production mode
if appconfig.Env == "development":
    running_mode = "  👩‍💻 🛠️  Running in::development mode"
else:
    app.add_middleware(HTTPSRedirectMiddleware)
    running_mode = "  🏭 ☁  Running in::production mode"


# Origins for CORS
origins = ["*"]

# Add middleware to allow CORS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST","GET","OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/health", status_code=status.HTTP_200_OK)  # endpoint for root URL
def Home():
    """
    Returns a dictionary containing information about the application.
    """
    return {
        "ApplicationName": app.title,
        "ApplicationOwner": "AISoC",
        "ApplicationVersion": "3.0.0",
        "ApplicationEngineer": "Sam Ayo",
        "ApplicationStatus": "running...",
    }


@app.post(f"{settings.API_STR}/chat", response_class=JSONResponse)
async def generate_response(
    data: ChatRequest,
    username: str = Depends(get_current_username),
) -> JSONResponse:
    """Endpoint for chat requests.
    It uses the StreamingConversationChain instance to generate responses,
    and then sends these responses as a streaming response.
    :param data: The request data.
    """
    try:
        data = data.model_dump()
        sentence = data.get("sentence").strip()
        # Basic attack protection: remove "[INST]" or "[/INST]" or "<|im_start|>"from the sentence
        sentence = re.sub(r"\[/?INST\]|<\|im_start\|>|<\|im_end\|>", "", sentence)
        stc = StreamConversation(llm=api_llm)
        task = asyncio.create_task(
        stc.generate_response(data.get("userId"),sentence)
        )
        agent_response = await task
        return JSONResponse(
                agent_response, 200
            )  # Return the agent response as JSONResponse
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {e}",
        )



# Main function to run the FastAPI server
async def main():
    config = uvicorn.Config(
        app,
        port=8000,
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()


# Run the FastAPI server if this script is executed
if __name__ == "__main__":
    asyncio.run(main())
