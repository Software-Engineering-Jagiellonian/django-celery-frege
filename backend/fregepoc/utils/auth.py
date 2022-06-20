from typing import Any, Dict

from channels.db import database_sync_to_async
from djangochannelsrestframework.permissions import BasePermission
from rest_framework_api_key.models import APIKey


class HasAPIKeyAsync(BasePermission):
    model = APIKey

    @database_sync_to_async
    def _has_permission(self, key) -> bool:
        return self.model.objects.is_valid(key)

    async def has_permission(
        self, scope: Dict[str, Any], consumer, action: str, **kwargs
    ) -> bool:
        if "api_key" not in kwargs:
            return False
        key = kwargs["api_key"]
        return await self._has_permission(key)
