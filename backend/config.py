"""
Configuration and utilities module for common functions.
"""

import os
import logging
from pathlib import Path
from typing import Optional


class Config:
    """Application configuration."""
    
    # Directories
    WORKSPACE_DIR = Path("workspace")
    MEMORY_DIR = Path("memory")
    BACKEND_DIR = Path("backend")
    FRONTEND_DIR = Path("frontend")
    
    # API
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # GitHub
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        for directory in [cls.WORKSPACE_DIR, cls.MEMORY_DIR]:
            directory.mkdir(exist_ok=True, parents=True)
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration."""
        if cls.GITHUB_TOKEN and not cls.GITHUB_USERNAME:
            logging.warning("GITHUB_TOKEN set but GITHUB_USERNAME missing")
            return False
        return True


def setup_logging(name: str = "ai_project_generator", 
                  level: Optional[str] = None) -> logging.Logger:
    """Setup logging configuration."""
    if level is None:
        level = Config.LOG_LEVEL
    
    logger = logging.getLogger(name)
    
    # Only add handler if not already added
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    logger.setLevel(getattr(logging, level))
    return logger


def get_project_path(project_name: str) -> Path:
    """Get full path to project."""
    return Config.WORKSPACE_DIR / project_name


def is_valid_identifier(name: str) -> bool:
    """Check if name is valid Python identifier."""
    return name.isidentifier() and not name.startswith('_')


def sanitize_name(name: str) -> str:
    """Sanitize name for use as filename/identifier."""
    # Replace spaces and special chars with underscore
    sanitized = name.lower()
    for char in [' ', '-', '.', '/']:
        sanitized = sanitized.replace(char, '_')
    
    # Remove non-alphanumeric
    sanitized = ''.join(c for c in sanitized if c.isalnum() or c == '_')
    
    # Ensure starts with letter or underscore
    if sanitized and not (sanitized[0].isalpha() or sanitized[0] == '_'):
        sanitized = '_' + sanitized
    
    return sanitized or "project"


# Initialize on import
Config.ensure_directories()
logger = setup_logging()
