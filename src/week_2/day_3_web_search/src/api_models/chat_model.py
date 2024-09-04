
from pydantic import BaseModel

class UserData(BaseModel):
    name: str

class ChatRequest(BaseModel):
    """Request model for chat requests.
    the message from the user.
    """
    sentence: str
    userId: str
