import os
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

# Load .env file from parent directory
load_dotenv(os.path.join(os.path.dirname(os.getcwd()), '.env'))

class Settings(BaseSettings):
    PROJECT_NAME: str = "AIVFX"
    API_V1_STR: str = "/api/v1"
    
    # Storage
    JOBS_DIR: str = os.path.join(os.path.dirname(os.getcwd()), "jobs")
    OUTPUTS_DIR: str = os.path.join(os.path.dirname(os.getcwd()), "outputs")
    
    # API Keys
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    LTX_API_KEY: Optional[str] = os.getenv("LTX_API_KEY")
    
    # Redis / Celery
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # ML Models
    USE_GPU: bool = os.getenv("USE_GPU", "true").lower() == "true"
    DEVICE: str = "cuda" if USE_GPU else "cpu"
    
    class Config:
        case_sensitive = True

settings = Settings()

# Ensure directories exist
os.makedirs(settings.JOBS_DIR, exist_ok=True)
os.makedirs(settings.OUTPUTS_DIR, exist_ok=True)
