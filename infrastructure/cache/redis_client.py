from typing import Optional

import redis.asyncio as redis


class RedisClient:
    def __init__(self, host: str, port: int, db: int) -> None:
        self._host = host
        self._port = port
        self._db = db
        self._client: Optional[redis.Redis] = None

    async def connect(self) -> None:
        """Connect to Redis."""
        self._client = redis.Redis(
            host=self._host,
            port=self._port,
            db=self._db,
            decode_responses=True,
        )

    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self._client:
            await self._client.close()

    async def get(self, key: str) -> Optional[str]:
        """Get a value from Redis."""
        if not self._client:
            raise RuntimeError("Redis client not connected")
        return await self._client.get(key)

    async def set(
        self,
        key: str,
        value: str,
        ttl: Optional[int] = None,
    ) -> None:
        """Set a value in Redis."""
        if not self._client:
            raise RuntimeError("Redis client not connected")
        await self._client.set(key, value, ex=ttl)

    async def delete(self, key: str) -> None:
        """Delete a key from Redis."""
        if not self._client:
            raise RuntimeError("Redis client not connected")
        await self._client.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if a key exists in Redis."""
        if not self._client:
            raise RuntimeError("Redis client not connected")
        return await self._client.exists(key) > 0

    async def keys(self, pattern: str) -> list[str]:
        """Get keys matching a pattern."""
        if not self._client:
            raise RuntimeError("Redis client not connected")
        return await self._client.keys(pattern)
