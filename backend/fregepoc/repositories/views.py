from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from rest_framework_api_key.permissions import HasAPIKey

from fregepoc.repositories.models import Repository, RepositoryFile
from fregepoc.repositories.serializers import (
    RepositoryFileSerializer,
    RepositorySerializer,
)


class RepositoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    permission_classes = [DjangoModelPermissions | HasAPIKey]
    filterset_fields = ["analyzed"]


class RepositoryFileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RepositoryFile.objects.all()
    serializer_class = RepositoryFileSerializer
    permission_classes = [DjangoModelPermissions | HasAPIKey]
    filterset_fields = ["repository", "analyzed", "language"]
