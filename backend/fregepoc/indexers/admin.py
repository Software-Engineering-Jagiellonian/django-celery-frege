import contextlib

from django.contrib import admin

from fregepoc.indexers.base import indexers
from fregepoc.utils.admin import AutoModelAdmin

# Adapted from:
# https://medium.com/hackernoon/automatically-register-all-models-in-django-admin-django-tips-481382cf75e5

for indexer_model in indexers:
    with contextlib.suppress(admin.sites.AlreadyRegistered):
        admin.site.register(indexer_model, AutoModelAdmin)
