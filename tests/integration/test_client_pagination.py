import pytest

from fossil.api import GitHubClient


@pytest.fixture
def client() -> GitHubClient:
    return GitHubClient(token="fake", max_retries=0)


def test_paginate_follows_next_link(client: GitHubClient, httpx_mock) -> None:  # type: ignore[no-untyped-def]
    base = "https://api.github.com"
    httpx_mock.add_response(
        url=f"{base}/items?per_page=100",
        json=[{"id": 1}, {"id": 2}],
        headers={"Link": f'<{base}/items?page=2>; rel="next"'},
    )
    httpx_mock.add_response(
        url=f"{base}/items?page=2",
        json=[{"id": 3}],
    )
    items = list(client.paginate("/items"))
    assert [i["id"] for i in items] == [1, 2, 3]


def test_paginate_respects_max_items(client: GitHubClient, httpx_mock) -> None:  # type: ignore[no-untyped-def]
    httpx_mock.add_response(
        json=[{"id": i} for i in range(100)],
    )
    items = list(client.paginate("/items", max_items=5))
    assert len(items) == 5
