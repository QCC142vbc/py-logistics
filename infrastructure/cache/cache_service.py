import json
from typing import Optional

from src.domain.inventory.models import Item
from src.infrastructure.cache.redis_client import RedisClient


class CacheService:
    def __init__(self, redis_client: RedisClient) -> None:
        self._redis = redis_client

    async def get_item(self, item_id: str) -> Optional[Item]:
        """Get an item from cache."""
        key = f"item:{item_id}"
        cached = await self._redis.get(key)
        if cached:
            data = json.loads(cached)
            return Item(**data)
        return None

    async def set_item(
        self,
        item_id: str,
        item: Item,
        ttl: int = 3600,
    ) -> None:
        """Set an item in cache."""
        key = f"item:{item_id}"
        data = {
            "id": item.id,
            "sku": item.sku,
            "name": item.name,
            "quantity": item.quantity,
            "unit_cost": str(item.unit_cost),
            "location": item.location,
            "category": item.category,
            "reorder_point": item.reorder_point,
            "lead_time_days": item.lead_time_days,
        }
        await self._redis.set(key, json.dumps(data), ttl)

    async def invalidate_pattern(self, pattern: str) -> None:
        """Invalidate all keys matching a pattern."""
        keys = await self._redis.keys(pattern)
        for key in keys:
            await self._redis.delete(key)
