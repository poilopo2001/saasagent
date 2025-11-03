"""
Configuration centralisée pour SaaS Generator v3
Gère toutes les variables d'environnement et les paramètres de configuration
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuration de l'application"""

    # API Keys
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    github_token: Optional[str] = os.getenv("GITHUB_TOKEN")
    vercel_token: Optional[str] = os.getenv("VERCEL_TOKEN")

    # Application
    app_title: str = "SaaS Generator v3 API"
    app_version: str = "3.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    # CORS
    cors_origins: list = ["*"]

    # Directories
    output_dir: str = "/tmp/generated-sites"

    # Agent Configuration
    agent_model: str = "claude-sonnet-4-5-20250929"
    agent_timeout: int = 600  # 10 minutes

    # Validation
    max_validation_attempts: int = 3

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Retourne une instance singleton des settings
    L'utilisation de lru_cache assure qu'on ne crée qu'une seule instance
    """
    return Settings()
