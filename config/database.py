from pydantic import BaseSettings


class DatabaseConfig(BaseSettings):
    """Database configuration."""

    host: str = "localhost"
    port: int = 5432
    database: str = "logistics_db"
    username: str = "logistics"
    password: str = "password"

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

    class Config:
        env_prefix = "DATABASE_"
