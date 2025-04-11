"""
Automatically registers all indexer models with the Django admin interface using a custom admin class.

This script loops through all models defined in the `indexers` list (imported from `frege.indexers.base`)
and registers each one with Django's admin site using the `AutoModelAdmin` class from `frege.utils.admin`.

If a model is already registered with the admin, the `AlreadyRegistered` exception is gracefully suppressed 
to avoid runtime errors.

Adapted from:
https://medium.com/hackernoon/automatically-register-all-models-in-django-admin-django-tips-481382cf75e5
"""

import contextlib

from django.contrib import admin

from frege.indexers.base import indexers
from frege.utils.admin import AutoModelAdmin

for indexer_model in indexers:
    with contextlib.suppress(admin.sites.AlreadyRegistered):
        admin.site.register(indexer_model, AutoModelAdmin)
