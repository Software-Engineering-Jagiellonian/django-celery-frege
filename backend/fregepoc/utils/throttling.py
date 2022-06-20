from rest_framework.throttling import SimpleRateThrottle
from rest_framework_api_key.permissions import KeyParser


class ApiKeyRateThrottle(SimpleRateThrottle):
    scope = "apikey"

    def get_cache_key(self, request, view):
        key = KeyParser().get(request)
        if key:
            ident = key
        else:
            ident = self.get_ident(request)

        return self.cache_format % {"scope": self.scope, "ident": ident}
