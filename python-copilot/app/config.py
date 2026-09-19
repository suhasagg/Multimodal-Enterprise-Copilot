from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    openai_api_key:str
    openai_model:str="gpt-5.6-luna"
    vision_model:str="gpt-5.6-luna"
    embedding_model:str="text-embedding-3-small"
    database_url:str="postgresql+asyncpg://copilot:copilot@localhost:5432/copilot"
    redis_url:str="redis://localhost:6379/0"
    java_mcp_url:str="http://localhost:8081/mcp"
    max_upload_mb:int=15
    otel_exporter_otlp_endpoint:str="http://localhost:4318"
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
settings=Settings()
