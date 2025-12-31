import time
from abc import ABC, abstractmethod

from src.caching_proxy.schemas import CachedBucket, DataToCache


class Cache(ABC):
    @abstractmethod
    def getval(self, key) -> None | DataToCache:
        raise NotImplementedError

    @abstractmethod
    def setval(self, key: str, value: DataToCache, ttl: int = 0) -> None:
        raise NotImplementedError

    @abstractmethod
    def delval(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def keys(self) -> list[str]:
        raise NotImplementedError


class InMemoryCache(Cache):
    def __init__(self) -> None:
        self._store: dict[str, CachedBucket] = {}

    def getval(self, key) -> None | DataToCache:
        entry: CachedBucket | None = self._store.get(key, None)
        if not entry:
            return None

        if entry.ttl and entry.expires_at and entry.expires_at < time.time():
            del self._store[key]
            return None

        return entry.value

    def setval(self, key: str, value: DataToCache, ttl: int = 0) -> None:
        bucket = CachedBucket(ttl=ttl, value=value)
        if ttl:
            bucket.expires_at = time.time() + ttl
        self._store[key] = bucket

    def delval(self, key: str) -> None:
        if key in self._store:
            del self._store[key]

    def clear(self) -> None:
        self._store.clear()

    @property
    def keys(self) -> list[str]:
        return list(self._store.keys())


cache = InMemoryCache()
