import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# --- Path finding ---
env_path = Path(__file__).parent.parent / '.env'

if env_path.exists():
    load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database
    DATABASE_URL: str

    # Firebase
    FIREBASE_SERVICE_ACCOUNT_JSON_BASE64: str

    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    # AI Services (Serper and HuggingFace are no longer used but we keep them for structure)
    HUGGINGFACE_API_TOKEN: str
    SERPER_API_KEY: str

    # --- NEW: Chatbase Credentials ---
    CHATBASE_API_KEY: str
    CHATBASE_SECRET_KEY: str

    class Config:
        case_sensitive = True

# Create a single instance of the settings to be used throughout the app
try:
    settings = Settings()
except Exception as e:
    print("❌ ERROR: Failed to create settings object. Make sure all required variables are in your .env file.")
    raise e