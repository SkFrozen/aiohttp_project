import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    REDIS_USERNAME: str
    REDIS_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    def get_db_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    def get_redis_url(self):
        return (
            f"redis://{self.REDIS_USERNAME}:{self.REDIS_PASSWORD}@"
            f"{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        )

    def write_secret_key(self, key: bytes):
        with open(".env", "ab") as f:
            f.write(f"SECRET_KEY={key}\n")


settings = Settings()
