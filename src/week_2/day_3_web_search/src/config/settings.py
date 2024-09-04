# encoding: utf-8
from pydantic_settings import BaseSettings,SettingsConfigDict
from src.config import appconfig



class Settings(BaseSettings):
    """
    This class extends the BaseSettings class from FastAPI.
    It contains the project definitions.

    Args:
        None.

    Returns:
        class: extends the settings class.
    """
    #app_config : SettingsConfigDict = SettingsConfigDict(env_file=(".env",".env.prod"))

    if appconfig.Env == "development":
        API_STR: str = "/dev/api/v1"
    else:
        API_STR: str = "/api/v1"

    VERSION: str = "3.0.2"
    
    PROJECT_NAME: str = "AI Server"

  

def get_setting():
    """
    Return the settings object.

    Args:
        None.

    Returns:
        class: extends the settings class.
    """
    return Settings()

