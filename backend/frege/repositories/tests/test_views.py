import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate

from frege.repositories.factories import (
    RepositoryFactory,
    RepositoryFileFactory,
)
from frege.repositories.serializers import (
    RepositoryFileSerializer,
    RepositorySerializer,
)
from frege.repositories.views import (
    RepositoryFileViewSet,
    RepositoryViewSet,
)


@pytest.fixture()
def sample_user():
    return User.objects.create(
        username="alice",
        first_name="Alice",
        last_name="Smith",
        email="alice@example.com",
    )


@pytest.fixture()
def sample_repositories():
    repo1 = RepositoryFactory()
    repo2 = RepositoryFactory(analyzed=True)
    return [repo1, repo2]


@pytest.fixture()
def sample_repository_file():
    return RepositoryFileFactory()


@pytest.mark.django_db
class TestRepositoryViewSet:
    def test_list_view(self, sample_user, sample_repositories):
        view = RepositoryViewSet.as_view({"get": "list"})
        request = APIRequestFactory().get("")
        force_authenticate(request, sample_user)
        response = view(request)

        assert response.status_code == 200
        assert response.data["next"] is None
        assert response.data["previous"] is None
        assert response.data["count"] == 2

        
        expected_data = RepositorySerializer(sample_repositories, many=True).data
        actual_data = response.data["results"]
        assert len(actual_data) == len(expected_data)
        assert all(item in actual_data for item in expected_data)

    def test_detail_view(self, sample_user, sample_repositories):
        view = RepositoryViewSet.as_view({"get": "retrieve"})
        request = APIRequestFactory().get("")
        force_authenticate(request, sample_user)
        sample_repository = sample_repositories[0]
        response = view(request, pk=sample_repository.pk)

        assert response.status_code == 200

        expected_data = RepositorySerializer(sample_repository).data
        actual_data = response.data
        assert expected_data == actual_data
    
    def test_list_view_unauthorized(self, sample_repositories):
        view = RepositoryViewSet.as_view({"get": "list"})
        request = APIRequestFactory().get("")
        response = view(request)

        assert (
            response.status_code in [401, 403]
        ), "Unauthorized users should not be able to access the list view"
    
    def test_detail_view_unauthorized(self, sample_repositories):
        view = RepositoryViewSet.as_view({"get": "retrieve"})
        request = APIRequestFactory().get("")
        sample_repository = sample_repositories[0]
        response = view(request, pk=sample_repository.pk)
        assert (
            response.status_code in [401, 403]
        ), "Unauthorized users should not be able to access the detail view"
    
    def test_list_view_analyzed(self, sample_user, sample_repositories):
        view = RepositoryViewSet.as_view({"get": "list"})
        request = APIRequestFactory().get("?analyzed=true")
        force_authenticate(request, sample_user)
        response = view(request)

        assert response.status_code == 200
        assert response.data["next"] is None
        assert response.data["previous"] is None
        assert response.data["count"] == 1, f"{response.data}"

        expected_data = RepositorySerializer(
            [sample_repositories[1]], many=True
        ).data
        actual_data = response.data["results"]
        assert len(actual_data) == len(expected_data)
        assert all(item in actual_data for item in expected_data)



@pytest.mark.django_db
class TestRepositoryFileViewSet:
    def test_list_view(self, sample_user, sample_repository_file):
        view = RepositoryFileViewSet.as_view({"get": "list"})
        request = APIRequestFactory().get("")
        force_authenticate(request, sample_user)
        response = view(request)
        assert response.status_code == 200
        assert response.data["next"] is None
        assert response.data["previous"] is None
        assert response.data["count"] == 1
        expected_data = RepositoryFileSerializer(sample_repository_file).data
        actual_data = response.data["results"][0]
        assert expected_data == actual_data

    def test_detail_view(self, sample_user, sample_repository_file):
        view = RepositoryFileViewSet.as_view({"get": "retrieve"})
        request = APIRequestFactory().get("")
        force_authenticate(request, sample_user)
        response = view(request, pk=sample_repository_file.pk)
        assert response.status_code == 200
        expected_data = RepositoryFileSerializer(sample_repository_file).data
        actual_data = response.data
        assert expected_data == actual_data
