from dataclasses import dataclass
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    username: str
    password: str

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class DatabaseConnection:
    def __init__(self, config: DatabaseConfig) -> None:
        self._config = config
        self._engine = None
        self._session_factory = None

    async def connect(self) -> None:
        """Establish database connection."""
        self._engine = create_async_engine(
            self._config.url,
            echo=False,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
        )
        self._session_factory = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def disconnect(self) -> None:
        """Close database connection."""
        if self._engine:
            await self._engine.dispose()

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session."""
        if not self._session_factory:
            raise RuntimeError("Database not connected. Call connect() first.")
        
        async with self._session_factory() as session:
            yield session

    @property
    def engine(self):
        """Get the database engine."""
        return self._engine
