import json
from pydantic import BaseModel
from llama_index.llms.groq import Groq
from llama_index.llms.vertex import Vertex
from llama_index.llms.anthropic import Anthropic
# from src.week_3.day_4_robust_rag.utils.anthropic_base import Anthropic
from anthropic import AnthropicVertex
from google.oauth2 import service_account
# import google.auth as google_auth


class LLMClient(BaseModel):

    groq_api_key: str = ""
    # credentials: service_account.Credentials = None
    secrets_path: str = None
    temperature: float = 0.1
    max_output_tokens: int = 512


    def load_credentials(self):
        with open(self.secrets_path, "r") as file:
            secrets = json.load(file)
        
        credentials = service_account.Credentials.from_service_account_info(
            secrets,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )

        return credentials

    def refresh_auth(self, credentials) -> None:
        
        """This is part of a workaround to resolve issues with authentication scopes for AnthropicVertex"""
        
        from google.auth.transport.requests import Request  # type: ignore[import-untyped]
        credentials.refresh(Request())

        return credentials

    def generate_access_token(self, credentials) -> str:

        """This is part of a workaround to resolve issues with authentication scopes for AnthropicVertex"""
        
        _credentials = self.refresh_auth(credentials)
        access_token = _credentials.token
        # print(access_token)

        if not access_token:
            raise RuntimeError("Could not resolve API token from the environment")

        assert isinstance(access_token, str)
        return access_token


    def groq(self, model):
        return Groq(
            model, 
            api_key=self.groq_api_key, 
            temperature=self.temperature,
            max_tokens=self.max_output_tokens
        )
        
    def gemini(self, model):
        credentials = self.load_credentials()

        return Vertex(
            model=model,
            project=credentials.project_id,
            credentials=credentials,
            temperature=self.temperature,
            max_tokens=self.max_output_tokens
        )

    def anthropic(self, model):

        credentials = self.load_credentials()
        access_token = self.generate_access_token(credentials)

        region_mapping = {
            "claude-3-5-sonnet@20240620": "us-east5",
            "claude-3-haiku@20240307": "us-central1",
            "claude-3-opus@20240229": "us-central1",
        }

        vertex_client = AnthropicVertex(
            access_token=access_token,
            project_id=credentials.project_id,
            region=region_mapping.get(model)
        )

        return Anthropic(
            model=model,
            vertex_client=vertex_client,
            temperature=self.temperature,
            max_tokens=self.max_output_tokens
        )
    
    def map_client_to_model(self, model):

        model_mapping = {
            "llama-3.1-70b-versatile": self.groq,
            "llama-3.1-8b-instant": self.groq,
            "mixtral-8x7b-32768": self.groq,
            "claude-3-5-sonnet@20240620": self.anthropic,
            "claude-3-haiku@20240307": self.anthropic,
            "claude-3-3-opus@20240229": self.anthropic,
            "gemini-1.5-flash": self.gemini,
            "gemini-1.5-pro": self.gemini,
        }

        _client = model_mapping.get(model)

        return _client(model)




