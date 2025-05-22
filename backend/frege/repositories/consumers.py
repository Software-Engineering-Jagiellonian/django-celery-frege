from djangochannelsrestframework.consumers import AsyncAPIConsumer
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.permissions import IsAuthenticated

from frege.repositories.models import Repository, RepositoryFile, CommitMessage, RepositoryCommitMessagesQuality
from frege.repositories.serializers import (
    RepositoryFileSerializer,
    RepositorySerializer, CommitMessageSerializer, RepositoryCommitMessagesQualitySerializer,
)
from frege.utils.auth import HasAPIKeyAsync


class LiveStatusConsumer(AsyncAPIConsumer):
    permission_classes = [HasAPIKeyAsync | IsAuthenticated]

    @model_observer(RepositoryFile, serializer_class=RepositoryFileSerializer)
    async def repository_file_change(
        self,
        message: RepositoryFileSerializer,
        action,
        subscribing_request_ids,
        **_,
    ):
        
        """
        Handles changes to repository files and broadcasts the update to subscribing clients.

        Args:
            message (RepositoryFileSerializer): The updated repository file data.
            action (str): The action performed (e.g., create, update, delete).
            subscribing_request_ids (list): List of request IDs of clients subscribing to this data.
        """
        for request_id in subscribing_request_ids:
            await self.reply(
                data=message,
                action=f"repository_file/{action}",
                request_id=request_id,
            )

    @action()
    async def subscribe_to_repository_file_activity(self, request_id, **_):
        """
        Subscribes the client to updates on repository file changes.

        Args:
            request_id (str): The unique ID of the subscription request.
        """
        await self.repository_file_change.subscribe(request_id=request_id)

    @model_observer(RepositoryCommitMessagesQuality, serializer_class=RepositoryCommitMessagesQualitySerializer)
    async def repository_commit_message_quality_change(
            self,
            message: RepositoryCommitMessagesQualitySerializer,
            action,
            subscribing_request_ids,
            **_,
    ):
        
        """
        Handles changes to the quality of commit messages and broadcasts updates to subscribing clients.

        Args:
            message (RepositoryCommitMessagesQualitySerializer): The updated commit message quality data.
            action (str): The action performed (e.g., create, update, delete).
            subscribing_request_ids (list): List of request IDs of clients subscribing to this data.
        """
        for request_id in subscribing_request_ids:
            await self.reply(
                data=message,
                action=f"repository_commit_messages_quality/{action}",
                request_id=request_id,
            )

    @action()
    async def subscribe_to_repository_commit_message_quality_change_activity(self, request_id, **_):
        """
        Subscribes the client to updates on repository commit message quality changes.

        Args:
            request_id (str): The unique ID of the subscription request.
        """
        await self.repository_commit_message_quality_change.subscribe(request_id=request_id)

    @model_observer(CommitMessage, serializer_class=CommitMessageSerializer)
    async def commit_message_change(
            self,
            message: CommitMessageSerializer,
            action,
            subscribing_request_ids,
            **_,
    ):
        
        """
        Handles changes to commit messages and broadcasts the update to subscribing clients.

        Args:
            message (CommitMessageSerializer): The updated commit message data.
            action (str): The action performed (e.g., create, update, delete).
            subscribing_request_ids (list): List of request IDs of clients subscribing to this data.
        """
        for request_id in subscribing_request_ids:
            await self.reply(
                data=message,
                action=f"commit_message/{action}",
                request_id=request_id,
            )

    @action()
    async def subscribe_to_commit_message_activity(self, request_id, **_):
        """
        Subscribes the client to updates on commit message changes.

        Args:
            request_id (str): The unique ID of the subscription request.
        """
        await self.commit_message_change.subscribe(request_id=request_id)

    @model_observer(Repository, serializer_class=RepositorySerializer)
    async def repository_change(
        self,
        message: RepositorySerializer,
        action,
        subscribing_request_ids,
        **_,
    ):
        """
        Handles changes to repository data and broadcasts the update to subscribing clients.

        Args:
            message (RepositorySerializer): The updated repository data.
            action (str): The action performed (e.g., create, update, delete).
            subscribing_request_ids (list): List of request IDs of clients subscribing to this data.
        """
        for request_id in subscribing_request_ids:
            await self.reply(
                data=message,
                action=f"repository/{action}",
                request_id=request_id,
            )

    @action()
    async def subscribe_to_repository_activity(self, request_id, **_):
        """
        Subscribes the client to updates on repository changes.

        Args:
            request_id (str): The unique ID of the subscription request.
        """
        await self.repository_change.subscribe(request_id=request_id)
