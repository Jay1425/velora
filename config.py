"""
Configuration classes for Velora Flask application.
Supports both development (SQLite) and production (PostgreSQL) environments.
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base configuration with common settings."""
    
    # Security Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24).hex())
    
    # CSRF Configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # No time limit for CSRF tokens
    
    # Session Configuration
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    
    # Database Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Admin Credentials
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH')
    
    # Rate Limiting
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = timedelta(minutes=15)


class DevelopmentConfig(Config):
    """Development configuration - uses SQLite."""
    
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # Allow HTTP in development
    
    # SQLite database for local development
    SQLALCHEMY_DATABASE_URI = 'sqlite:///velora.db'


class ProductionConfig(Config):
    """Production configuration - uses PostgreSQL via DATABASE_URL."""
    
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # Require HTTPS in production
    
    # CSRF Configuration for production (enforce SSL)
    WTF_CSRF_SSL_STRICT = True  # Require HTTPS for CSRF validation in production
    
    # PostgreSQL database URL from environment (Neon compatible)
    DATABASE_URL = os.environ.get("DATABASE_URL")
    
    if DATABASE_URL:
        # Convert postgres:// to postgresql:// for Neon compatibility
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Fallback to SQLite if DATABASE_URL not set
        SQLALCHEMY_DATABASE_URI = 'sqlite:///velora.db'
    
    # PostgreSQL connection pool configuration
    if SQLALCHEMY_DATABASE_URI.startswith("postgresql://"):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,       # Verify connections before using
            "pool_recycle": 300,          # Recycle connections after 5 minutes
            "pool_size": 10,              # Max connections in pool
            "max_overflow": 20            # Max overflow connections
        }


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
