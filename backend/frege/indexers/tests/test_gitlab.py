import pytest
from unittest.mock import patch, Mock
from frege.indexers.utils.gitlab import Client, RateLimitExceededException
from frege.indexers.models import GitLabIndexer

BASE_ENDPOINT = "https://gitlab.com/api/v4/projects"

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
    mock_response.json.return_value = [{"id": "abc123"}]
    mock_response.headers = {}
    mock_get.return_value = mock_response

    commit = client._commit_hash(project_id=101)

    assert commit == "abc123"
    mock_get.assert_called_once()
    assert "projects/101/repository/commits" in mock_get.call_args[0][0]


@patch("frege.indexers.utils.gitlab.requests.get")
def test_commit_hash_handles_empty_commits(mock_get, client, caplog):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_response.headers = {}
    mock_get.return_value = mock_response

    with caplog.at_level("INFO"):
        commit = client._commit_hash(project_id=202)

    assert commit is None
    assert "No commits found for project 202" in caplog.text


@patch("frege.indexers.utils.gitlab.requests.get")
def test_commit_hash_handles_non_200(mock_get, client, caplog):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.headers = {}
    mock_get.return_value = mock_response

    with caplog.at_level("INFO"):
        commit = client._commit_hash(project_id=303)

    assert commit is None
    assert "Unable to fetch commits for project 303" in caplog.text

@patch("frege.indexers.utils.gitlab.Client._get")
def test_projects_pagination(mock_get):
    """Test if _projects method correctly handles pagination across multiple pages"""

    first_response = Mock()
    first_response.json.return_value = [{"id": 1, "name": "Project 1"}, {"id": 2, "name": "Project 2"}]
    first_response.links = {"next": {"url": "https://gitlab.com/api/v4/projects/next-page"}}

    second_response = Mock()
    second_response.json.return_value = [{"id": 3, "name": "Project 3"}, {"id": 4, "name": "Project 4"}]
    second_response.links = {}

    mock_get.side_effect = [first_response, second_response]

    client = Client(_ratelimit_remaining=1000, token='dummy-token', after_id=0, min_forks=5, min_stars=10)
    
    results = list(client._projects())

    assert len(results) == 2
    assert results == [[{'id': 1, 'name': 'Project 1'}, {'id': 2, 'name': 'Project 2'}], [{'id': 3, 'name': 'Project 3'}, {'id': 4, 'name': 'Project 4'}]]

    assert mock_get.call_count == 2
    mock_get.assert_any_call(BASE_ENDPOINT, params={'pagination': 'keyset', 'per_page': '100', 'order_by': 'id', 'sort': 'asc', 'id_after': client.after_id})
    mock_get.assert_any_call("https://gitlab.com/api/v4/projects/next-page")

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


@pytest.mark.django_db
@patch("frege.indexers.models.Repository.objects.create")
@patch("frege.indexers.models._is_repo_unique", return_value=True)
@patch("frege.indexers.models.gitlab.Client.repositories")
def test_indexer_iter_yields_repo(mock_repositories, mock_unique, mock_create):
    mock_repo_data = {
        "git_url": "http://example.com/repo.git",
        "name": "Test Repo",
    }
    mock_repo = Mock()
    mock_create.return_value = mock_repo
    mock_repositories.return_value = iter([ (mock_repo_data, 1234) ])
    
    indexer = GitLabIndexer()
    indexer.save()

    result = list(indexer)
    
    assert result == [[mock_repo]]
    assert indexer.last_project_id == 1234
    mock_create.assert_called_once_with(**mock_repo_data)

@patch("frege.indexers.models._is_repo_unique", return_value=False)
@patch("frege.indexers.models.gitlab.Client.repositories")
def test_indexer_iter_skips_non_unique(mock_repositories, mock_unique):
    mock_repositories.return_value = iter([
        ({"git_url": "http://example.com/repo.git"}, 100)
    ])
    
    indexer = GitLabIndexer()
    result = list(indexer)
    
    assert result == []

@patch("frege.indexers.models.gitlab.Client.repositories", return_value=iter([]))
def test_indexer_iter_no_repos(mock_repositories):
    indexer = GitLabIndexer()
    result = list(indexer)
    assert result == []

@patch("frege.indexers.models.GitLabIndexer.save")
@patch("frege.indexers.models._is_repo_unique", return_value=True)
@patch("frege.indexers.models.gitlab.Client.repositories")
@patch("frege.indexers.models.Repository.objects.create", return_value=Mock())
def test_indexer_saves_after_repo(mock_create, mock_repositories, mock_unique, mock_save):
    mock_repositories.return_value = iter([
        ({"git_url": "http://example.com/repo.git"}, 42)
    ])
    indexer = GitLabIndexer()
    list(indexer)

    mock_save.assert_called_once_with(update_fields=["last_project_id"])
