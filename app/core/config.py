# core/settings.py
import logging

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

INSECURE_SECRET_KEY = "your-secret-key-here"


def _parse_cors_origins(value: str) -> list[str]:
    """Parse comma-separated CORS origins into a list, no empty strings."""
    return [x.strip() for x in value.split(",") if x.strip()]


class Settings(BaseSettings):
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    # Signs every access/refresh token. MUST be set in the environment as
    # SECRET_KEY — note that is the name the app reads, not JWT_SECRET.
    SECRET_KEY: str = INSECURE_SECRET_KEY
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Google OAuth
    GOOGLE_CLIENT_ID: str 
    GOOGLE_CLIENT_SECRET: str 
    GOOGLE_REDIRECT_URI: str 
    FRONTEND_URL: str = "http://localhost:3000"
    SESSION_SECRET_KEY: str = "change-me-in-production"
    ADMIN_EMAIL: str = "[EMAIL_ADDRESS]"

    # default uses asyncpg driver; override in .env in production
    EMAIL_HOST: str = "smtp.example.com"
    EMAIL_PORT: int = 587
    EMAIL_USER: str = "your_email@example.com"
    EMAIL_PASSWORD: str = "your_email_password"
    EMAIL_FROM: str = "your_email@example.com"
    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    # Comma-separated list of allowed frontend origins, e.g. https://myapp.vercel.app,https://myapp.com
    CORS_ORIGINS: str = (
        "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173,https://gdg-website-topaz-rho.vercel.app"
    )
    DEBUG: bool = False
    DATABASE_URL: str = "ppostgresql+asyncpg://postgres:maryjesu99@localhost:5432/gdg_db"

    model_config = {"env_file": ".env", "extra": "allow"}

    @property
    def cors_origins_list(self) -> list[str]:
        return _parse_cors_origins(self.CORS_ORIGINS)

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


settings = Settings()

if settings.SECRET_KEY == INSECURE_SECRET_KEY:
    # The fallback is committed to this repo, so anyone can forge a token —
    # including an admin one — while it's in use.
    logger.critical(
        "SECRET_KEY is unset and is falling back to the public default from the "
        "repo. Every JWT is forgeable. Set SECRET_KEY in the environment "
        "(the app reads SECRET_KEY, not JWT_SECRET)."
    )
