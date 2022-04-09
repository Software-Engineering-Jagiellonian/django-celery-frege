from django.contrib import admin

from fregepoc.indexers.models import GitHubIndexer


@admin.register(GitHubIndexer)
class GitHubIndexerAdmin(admin.ModelAdmin):
    list_display = (
        "min_forks",
        "min_stars",
        "current_page",
        "rate_limit_timeout",
    )
