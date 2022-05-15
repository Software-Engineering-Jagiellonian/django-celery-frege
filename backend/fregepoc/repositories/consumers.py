from djangochannelsrestframework.consumers import AsyncAPIConsumer
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.permissions import IsAuthenticated

from fregepoc.repositories.models import Repository, RepositoryFile
from fregepoc.repositories.serializers import (
    RepositoryFileSerializer,
    RepositorySerializer,
)
from fregepoc.utils.auth import HasAPIKeyAsync


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
        for request_id in subscribing_request_ids:
            await self.reply(
                data=message,
                action=f"repository_file/{action}",
                request_id=request_id,
            )

    @action()
    async def subscribe_to_repository_file_activity(self, request_id, **_):
        await self.repository_file_change.subscribe(request_id=request_id)

    @model_observer(Repository, serializer_class=RepositorySerializer)
    async def repository_change(
        self,
        message: RepositorySerializer,
        action,
        subscribing_request_ids,
        **_,
    ):
        for request_id in subscribing_request_ids:
            await self.reply(
                data=message,
                action=f"repository/{action}",
                request_id=request_id,
            )

    @action()
    async def subscribe_to_repository_activity(self, request_id, **_):
        await self.repository_change.subscribe(request_id=request_id)
