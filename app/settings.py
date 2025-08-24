from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    STRIPE_API_KEY: str = ""
    SECRET_KEY: str = "supersecret"
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Session settings
    SESSION_SECRET_KEY: str = "your-session-secret-key-here"
    SESSION_COOKIE_NAME: str = "koe_session"
    SESSION_COOKIE_SECURE: bool = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "lax"

    model_config = {"env_file": ".env"}

settings = Settings()
