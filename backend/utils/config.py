import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass
class Settings:
    """Application settings loaded from environment variables"""
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    backend_host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))
    frontend_port: int = int(os.getenv("FRONTEND_PORT", "8501"))

def get_settings() -> Settings:
    """Get application settings"""
    return Settings()

def validate_settings():
    """Validate that required settings are present"""
    settings = get_settings()
    
    if not settings.google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    
    return settings 