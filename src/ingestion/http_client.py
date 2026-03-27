from __future__ import annotations

from dataclasses import dataclass

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


@dataclass(frozen=True)
class RetryConfig:
    total: int = 4
    backoff_factor: float = 1.0
    timeout_seconds: int = 30


class RetryHttpClient:
    def __init__(self, retry_config: RetryConfig | None = None) -> None:
        self.retry_config = retry_config or RetryConfig()
        self.session = self._build_session(self.retry_config)

    @staticmethod
    def _build_session(retry_config: RetryConfig) -> requests.Session:
        retry = Retry(
            total=retry_config.total,
            connect=retry_config.total,
            read=retry_config.total,
            status=retry_config.total,
            backoff_factor=retry_config.backoff_factor,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"GET", "POST"}),
            raise_on_status=False,
        )

        adapter = HTTPAdapter(max_retries=retry)
        session = requests.Session()
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def get_json(self, url: str, params: dict[str, str] | None = None) -> dict:
        response = self.session.get(url, params=params, timeout=self.retry_config.timeout_seconds)
        response.raise_for_status()
        return response.json()

    def get_text(self, url: str, params: dict[str, str] | None = None) -> str:
        response = self.session.get(url, params=params, timeout=self.retry_config.timeout_seconds)
        response.raise_for_status()
        return response.text
