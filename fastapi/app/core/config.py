import re
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, HttpUrl, PostgresDsn, validator, Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    def __init__(self, **values: Any):
        super().__init__(**values)

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "App Home consumption datas"

    class Config:
        env_file = "../../.env"


settings = Settings()
    