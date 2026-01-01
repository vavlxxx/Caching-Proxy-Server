import posixpath
import sys
from pathlib import Path
from urllib.parse import urljoin

import httpx

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.caching_proxy.config import settings
from src.caching_proxy.schemas import AppStatus
from src.caching_proxy.utils import CachingHelper


class ProxyClient:
    def __init__(self, host: str):
        self.host = host

    def _build_url(self, port: int, endpoint: str) -> str:
        host_port = CachingHelper.join_host_and_port(self.host, port)
        return urljoin(host_port, posixpath.join(settings.API_PREFIX_MANAGEMENT, endpoint))

    def _request(self, method: str, port: int, endpoint: str, **kwargs) -> httpx.Response | None:
        url = self._build_url(port, endpoint)
        try:
            return httpx.request(method, url, headers=settings.HTTPX_HEADERS, timeout=1.0, **kwargs)
        except httpx.RequestError:
            return None

    def get_status(self, port: int) -> AppStatus | None:
        resp = self._request("GET", port, settings.API_PREFIX_HEALTH)
        if resp and resp.is_success:
            return AppStatus.model_validate(resp.json())
        return None

    def shutdown(self, port: int) -> bool:
        resp = self._request("POST", port, settings.API_PREFIX_SHUTDOWN)
        return resp is not None

    def clear_cache(self, port: int) -> bool:
        resp = self._request("POST", port, settings.API_PREFIX_CLEAR)
        return resp is not None

    def get_keys(self, port: int) -> list[tuple[str, float | None]]:
        resp = self._request("GET", port, settings.API_PREFIX_KEYS)
        if resp and resp.is_success:
            return resp.json().get("keys", [])
        return []


client = ProxyClient(settings.HOST)
