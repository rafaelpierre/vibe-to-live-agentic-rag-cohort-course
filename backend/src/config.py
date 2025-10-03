"""
Configuration management using Pydantic Settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    To use:
    1. Create a .env file in the project root
    2. Add your API keys and configuration
    3. Settings will be automatically loaded
    """

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"

    # Qdrant Configuration
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection_name: str = "course_documents"

    # Application Configuration
    app_name: str = "Agentic RAG API"
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# Global settings instance
settings = Settings()
