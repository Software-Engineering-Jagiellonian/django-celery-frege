from django.contrib import admin

from fregepoc.repositories.models import Repository, RepositoryFile


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = (
        "analyzed",
        "git_url",
        "repo_url",
        "commit_hash",
        "discovered_time",
        "fetch_time",
    )
    ordering = ("-discovered_time",)


@admin.register(RepositoryFile)
class RepositoryFileAdmin(admin.ModelAdmin):
    list_display = (
        "repository",
        "analyzed",
        "language",
        "repo_relative_file_path",
        "metrics",
        "analyzed_time",
    )
    ordering = ("-analyzed_time",)
