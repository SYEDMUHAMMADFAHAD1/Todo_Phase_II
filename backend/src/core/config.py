from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Todo App"
    API_V1_STR: str = "/api"

    # Database
    DATABASE_URL: str

    # Auth
    BETTER_AUTH_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Default to 30 minutes

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )


settings = Settings()
