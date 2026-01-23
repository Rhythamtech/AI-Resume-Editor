import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Centralized configuration management for the application."""
    
    def __init__(self):
        # LLM Configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.openai_base_url = os.getenv("OPENAI_BASE_URL")
        
        # Application Configuration
        self.default_temperature = 0.7
        self.templates_dir = "src/templates"
        
    def validate(self):
        """Validate required configuration."""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY must be set in environment variables")
        return True


# Global settings instance
settings = Settings()
