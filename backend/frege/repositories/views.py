from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from rest_framework_api_key.permissions import HasAPIKey

from frege.repositories.models import Repository, RepositoryFile, CommitMessage, RepositoryCommitMessagesQuality
from frege.repositories.serializers import (
    RepositoryFileSerializer,
    RepositorySerializer, CommitMessageSerializer, RepositoryCommitMessagesQualitySerializer,
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


class CommitMessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommitMessage.objects.all()
    serializer_class = CommitMessageSerializer
    permission_classes = [DjangoModelPermissions | HasAPIKey]
    filterset_fields = ["repository", "analyzed", "commit_hash", "commit_type", "fog_index"]


class RepositoryCommitMessagesQualityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RepositoryCommitMessagesQuality.objects.all()
    serializer_class = RepositoryCommitMessagesQualitySerializer
    permission_classes = [DjangoModelPermissions | HasAPIKey]
    filterset_fields = ["repository", "analyzed"]
