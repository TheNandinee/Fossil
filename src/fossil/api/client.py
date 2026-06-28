"""GitHub API client: authentication, retries, rate limiting, pagination.

This is the only module that talks to GitHub over HTTP. Everything else depends
on this abstraction, which makes the rest of the codebase trivially testable
with a mocked client.
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from typing import Any

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from fossil.config import get_logger, get_settings
from fossil.core.exceptions import (
    GitHubAPIError,
    NotFoundError,
    RateLimitError,
)

logger = get_logger(__name__)

_RETRYABLE = (httpx.TransportError, httpx.TimeoutException)


class GitHubClient:
    """A thin, typed wrapper over the GitHub REST + GraphQL APIs."""

    def __init__(
        self,
        token: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> None:
        settings = get_settings()
        self._token = token if token is not None else settings.github_token
        self._base_url = (base_url or settings.github_api_url).rstrip("/")
        self._timeout = timeout if timeout is not None else settings.request_timeout
        self._max_retries = (
            max_retries if max_retries is not None else settings.max_retries
        )
        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=self._timeout,
            headers=self._build_headers(),
        )

    def _build_headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "fossil-archaeology",
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    # -- lifecycle --------------------------------------------------------
    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> GitHubClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # -- rate limiting ----------------------------------------------------
    def _respect_rate_limit(self, response: httpx.Response) -> None:
        """Sleep if we are about to exhaust the rate limit window."""
        remaining = response.headers.get("X-RateLimit-Remaining")
        reset = response.headers.get("X-RateLimit-Reset")
        if remaining is None or reset is None:
            return
        if int(remaining) > 0:
            return
        sleep_for = max(0.0, float(reset) - time.time()) + 1.0
        logger.warning("Rate limit reached; sleeping %.0fs", sleep_for)
        time.sleep(sleep_for)

    # -- core request -----------------------------------------------------
    @retry(
        retry=retry_if_exception_type(_RETRYABLE),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=30),
        reraise=True,
    )
    def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        response = self._client.request(method, path, **kwargs)

        if response.status_code == 404:
            raise NotFoundError(f"Not found: {path}", status_code=404)

        if response.status_code in (403, 429):
            remaining = response.headers.get("X-RateLimit-Remaining")
            if remaining == "0":
                self._respect_rate_limit(response)
                # one retry after sleeping
                response = self._client.request(method, path, **kwargs)
            if response.status_code in (403, 429):
                raise RateLimitError(
                    "GitHub rate limit or access error",
                    status_code=response.status_code,
                )

        if response.status_code >= 400:
            raise GitHubAPIError(
                f"GitHub API error {response.status_code} for {path}: "
                f"{response.text[:200]}",
                status_code=response.status_code,
            )
        return response

    # -- REST helpers -----------------------------------------------------
    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """GET a single REST resource and return parsed JSON."""
        return self._request("GET", path, params=params).json()

    def paginate(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        *,
        max_items: int | None = None,
    ) -> Iterator[dict[str, Any]]:
        """Yield items across paginated REST list endpoints.

        Follows the ``Link: rel="next"`` header. Stops at ``max_items`` if set.
        """
        params = dict(params or {})
        params.setdefault("per_page", 100)
        url: str | None = path
        yielded = 0

        while url is not None:
            response = self._request("GET", url, params=params)
            params = None  # subsequent URLs already carry query params
            payload = response.json()
            items = payload if isinstance(payload, list) else payload.get("items", [])
            for item in items:
                yield item
                yielded += 1
                if max_items is not None and yielded >= max_items:
                    return
            url = self._next_link(response)

    @staticmethod
    def _next_link(response: httpx.Response) -> str | None:
        link = response.headers.get("Link")
        if not link:
            return None
        for part in link.split(","):
            section = part.split(";")
            if len(section) < 2:
                continue
            url_part = section[0].strip().lstrip("<").rstrip(">")
            rel_part = section[1].strip()
            if rel_part == 'rel="next"':
                return str(url_part)
        return None

    # -- GraphQL ----------------------------------------------------------
    def graphql(
        self, query: str, variables: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Execute a GraphQL query against GitHub's v4 API."""
        response = self._request(
            "POST",
            "/graphql",
            json={"query": query, "variables": variables or {}},
        )
        data: dict[str, Any] = response.json()
        if "errors" in data:
            raise GitHubAPIError(f"GraphQL error: {data['errors']}")
        result: dict[str, Any] = data["data"]
        return result
