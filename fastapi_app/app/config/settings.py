from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = Field(default_factory=str, validation_alias="DATABASE_URL")
    ENVIRONMENT: str = Field(default_factory=str, validation_alias="ENVIRONMENT")
    PROJECT_NAME: str = Field(default_factory=str, validation_alias="PROJECT_NAME")
    API_KEY: str = Field(..., validation_alias="API_KEY")
    log_level: str = Field("INFO", validation_alias="log_level")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings(log_level="INFO")
