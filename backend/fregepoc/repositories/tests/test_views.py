import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate

from fregepoc.repositories.factories import (
    RepositoryFactory,
    RepositoryFileFactory,
)
from fregepoc.repositories.serializers import (
    RepositoryFileSerializer,
    RepositorySerializer,
)
from fregepoc.repositories.views import (
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
def sample_repository():
    return RepositoryFactory()


@pytest.fixture()
def sample_repository_file():
    return RepositoryFileFactory()


@pytest.mark.django_db
class TestRepositoryViewSet:
    def test_list_view(self, sample_user, sample_repository):
        view = RepositoryViewSet.as_view({"get": "list"})
        request = APIRequestFactory().get("")
        force_authenticate(request, sample_user)
        response = view(request)
        assert response.status_code == 200
        assert response.data["next"] is None
        assert response.data["previous"] is None
        assert response.data["count"] == 1
        expected_data = RepositorySerializer(sample_repository).data
        actual_data = response.data["results"][0]
        assert expected_data == actual_data

    def test_detail_view(self, sample_user, sample_repository):
        view = RepositoryViewSet.as_view({"get": "retrieve"})
        request = APIRequestFactory().get("")
        force_authenticate(request, sample_user)
        response = view(request, pk=sample_repository.pk)
        assert response.status_code == 200
        expected_data = RepositorySerializer(sample_repository).data
        actual_data = response.data
        assert expected_data == actual_data


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
