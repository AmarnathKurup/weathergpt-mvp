"""A tiny in-memory TTL cache used instead of Redis for the MVP.

Not persistent, not distributed - just enough to avoid hammering
free external APIs during local development/demo usage.
"""
import time
from typing import Any, Optional


class TTLCache:
    def __init__(self, default_ttl: int = 600):
        self._store: dict[str, tuple[float, Any]] = {}
        self.default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        item = self._store.get(key)
        if item is None:
            return None
        expires_at, value = item
        if time.time() > expires_at:
            self._store.pop(key, None)
            return None
        return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        ttl = ttl if ttl is not None else self.default_ttl
        self._store[key] = (time.time() + ttl, value)

    def clear(self) -> None:
        self._store.clear()


# Single process-wide cache instance
cache = TTLCache()
