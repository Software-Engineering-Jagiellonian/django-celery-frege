import pytest
from unittest.mock import patch, Mock
from frege.indexers.utils.gitlab import Client, RateLimitExceededException

@pytest.fixture
def client():
    return Client(token="dummy-token", min_stars=10, min_forks=5)

@patch("frege.indexers.utils.gitlab.requests.get")
def test_get_adds_token_and_checks_limit(mock_get):
    client = Client(token="abc123", _ratelimit_remaining=1)
    mock_response = Mock()
    mock_response.headers = {'RateLimit-Remaining': '999'}
    mock_get.return_value = mock_response

    response = client._get("https://example.com")

    assert client.ratelimit_remaining == 999
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["headers"] == {"PRIVATE-TOKEN": "abc123"}
    assert response == mock_response


def test_get_raises_rate_limit():
    client = Client(_ratelimit_remaining=0)
    with pytest.raises(RateLimitExceededException):
        client._get("https://example.com")


@patch("frege.indexers.utils.gitlab.requests.get")
def test_commit_hash_success(mock_get, client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": "commit123"}]
    mock_get.return_value = mock_response

    commit_hash = client._commit_hash(123)

    assert commit_hash == "commit123"
    mock_get.assert_called_once()
    assert "projects/123/repository/commits" in mock_get.call_args[0][0]


@patch("frege.indexers.utils.gitlab.requests.get")
def test_commit_hash_empty_response(mock_get, client, caplog):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    with caplog.at_level("WARNING"):
        result = client._commit_hash(456)

    assert result is None
    assert "No commits found for project 456" in caplog.text


@patch("frege.indexers.utils.gitlab.requests.get")
def test_commit_hash_non_200_response(mock_get, client, caplog):
    mock_response = Mock()
    mock_response.status_code = 403
    mock_get.return_value = mock_response

    with caplog.at_level("WARNING"):
        result = client._commit_hash(789)

    assert result is None
    assert "Unable to fetch commits for project 789" in caplog.text


@patch("frege.indexers.utils.gitlab.requests.get")
def test_projects_pagination(mock_get, client):
    response_page_1 = Mock()
    response_page_1.json.return_value = [{"id": 1}]
    response_page_1.links = {"next": {"url": "https://next-page.com"}}
    response_page_1.headers = {}

    response_page_2 = Mock()
    response_page_2.json.return_value = [{"id": 2}]
    response_page_2.links = {}
    response_page_2.headers = {}

    mock_get.side_effect = [response_page_1, response_page_2]

    projects = list(client._projects())
    flat = list(chain.from_iterable(projects))

    assert [p["id"] for p in flat] == [2]


@patch("frege.indexers.utils.gitlab.Client._get")
@patch("frege.indexers.utils.gitlab.Client._commit_hash")
def test_repositories_filters_and_yields(mock_commit_hash, mock_get, client):
    mock_get.return_value = Mock(
        json=Mock(return_value=[
            {"id": 1, "star_count": 12, "forks_count": 6,
             "name": "test", "description": "desc",
             "http_url_to_repo": "git_url", "web_url": "web"}
        ]),
        links={}
    )
    mock_commit_hash.return_value = "abc123"

    repos = list(client.repositories())
    assert len(repos) == 1
    repo_data, repo_id = repos[0]
    assert repo_data["name"] == "test"
    assert repo_data["commit_hash"] == "abc123"
    assert repo_id == 1
