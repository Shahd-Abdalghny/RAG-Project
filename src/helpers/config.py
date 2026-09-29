from pydantic_settings import BaseSettings, SettingsConfigDict

# Application settings are loaded from the .env file.
class Settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    OPENAI_API_KEY:str
    FILE_ALLOWED_TYPES:list
    FILE_MAX_SIZE:int
    FILE_DEFAULT_CHUNK_SIZE:int 
    
    MONGODB_URI:str
    MONGODB_DB_NAME:str
    
    class Config:
        env_file = ".env"

# Return the environment-driven settings object used by the app.
def get_settings() -> Settings:
    return Settings()        
        