from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    port: int = 8000
    openai_api_key: str = ""
    model_name: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    search_provider: str = "bing"
    bing_api_key: str = ""
    vector_db_provider: str = "pinecone"
    pinecone_api_key: str = ""
    pinecone_env: str = ""
    pinecone_index: str = "ai-coder-agent"
    database_url: str = "sqlite:///./data.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
