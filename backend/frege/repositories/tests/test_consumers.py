import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from rest_framework_api_key.models import APIKey

from frege.repositories.consumers import LiveStatusConsumer
from frege.repositories.factories import (
    RepositoryFactory,
    RepositoryFileFactory,
)
from frege.repositories.serializers import (
    RepositoryFileSerializer,
    RepositorySerializer,
)   

async def show_queue(self):
    messages = []
    while not await self.receive_nothing():
        mess = await self.receive_json_from()
        messages.append(str(mess))
    return ",\n".join(messages)

WebsocketCommunicator.show_queue = show_queue

@pytest.fixture()
def api_key():
    _, key = APIKey.objects.create_key(name="test-key")
    return key

@pytest.fixture(autouse=True)
def use_test_channel_layer(settings):
    settings.CHANNEL_LAYERS = {
        "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
    }

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
class TestLiveStatusConsumer:
    @staticmethod
    @database_sync_to_async
    def _create_test_repository():
        return RepositoryFactory()

    @staticmethod
    @database_sync_to_async
    def _create_test_repository_file():
        return RepositoryFileFactory()

    @staticmethod
    async def _test_event_api(
        api_key, request_action, create_fn, response_action, serializer
    ):
        communicator = WebsocketCommunicator(
            LiveStatusConsumer.as_asgi(), "/ws/test-live-status/"
        )
        try:
            connected, subprotocol = await communicator.connect()
            assert connected
            await communicator.send_json_to(
                {"api_key": api_key, "action": request_action, "request_id": 1}
            )
            assert await communicator.receive_nothing(), await communicator.show_queue()
            file = await create_fn()
            response = await communicator.receive_json_from()
            assert response["response_status"] == 200
            assert response["request_id"] == 1
            assert response["action"] == response_action
            expected_data = serializer(file).data
            actual_data = response["data"]
            assert expected_data == actual_data
            assert await communicator.receive_nothing(), await communicator.show_queue()
        finally:
            await communicator.disconnect()

    async def test_subscribe_to_repository_file_activity(self, api_key):
        await self._test_event_api(
            api_key=api_key,
            request_action="subscribe_to_repository_file_activity",
            create_fn=self._create_test_repository_file,
            response_action="repository_file/create",
            serializer=RepositoryFileSerializer,
        )

    async def test_subscribe_to_repository_activity(self, api_key):
        await self._test_event_api(
            api_key=api_key,
            request_action="subscribe_to_repository_activity",
            create_fn=self._create_test_repository,
            response_action="repository/create",
            serializer=RepositorySerializer,
        )

    async def test_invalid_api_key(self):
        communicator = WebsocketCommunicator(
            LiveStatusConsumer.as_asgi(), "/ws/test-live-status/"
        )
        try:
            connected, _ = await communicator.connect()
            assert connected
            await communicator.send_json_to(
                {"api_key": "invalid_key", "action": "subscribe_to_repository_activity", "request_id": 1}
            )
            response = await communicator.receive_json_from()
            assert response["response_status"] == 403
            assert await communicator.receive_nothing(), await communicator.show_queue()
        finally:
            await communicator.disconnect()

    async def test_unknown_action(self, api_key):
        communicator = WebsocketCommunicator(
            LiveStatusConsumer.as_asgi(), "/ws/test-live-status/"
        )
        try:
            connected, _ = await communicator.connect()
            assert connected
            await communicator.send_json_to(
                {"api_key": api_key, "action": "non_existing_action", "request_id": 1}
            )
            response = await communicator.receive_json_from()
            assert response["response_status"] == 405
            assert await communicator.receive_nothing(), await communicator.show_queue()
        finally:
            await communicator.disconnect()