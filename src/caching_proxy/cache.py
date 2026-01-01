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
    def keys(self) -> list[tuple[str, float | None]]:
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
    def keys(self) -> list[tuple[str, float | None]]:
        cache_items = list(self._store.items())
        relevant_items = list(
            filter(
                lambda item: not item[1].ttl or item[1].expires_at and item[1].expires_at > time.time(),
                cache_items,
            ),
        )
        self._store = dict(relevant_items)
        return list(map(lambda item: (item[0], item[1].expires_at), relevant_items))


cache = InMemoryCache()
