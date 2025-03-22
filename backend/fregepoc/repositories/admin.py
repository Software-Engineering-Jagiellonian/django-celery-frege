from django.contrib import admin

from fregepoc.repositories.models import Repository, RepositoryFile, CommitMessage, RepositoryCommitMessagesQuality


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
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


@admin.register(RepositoryCommitMessagesQuality)
class RepositoryCommitMessagesQualityAdmin(admin.ModelAdmin):
    list_display = (
        "repository",
        "analyzed",
        "commits_amount",
        "average_commit_message_characters_length",
        "average_commit_message_words_amount",
        "average_commit_message_fog_index",
        "classifiable_to_unclassifiable_commit_messages_ratio",
        "percentage_of_feature_commits",
        "percentage_of_fix_commits",
        "percentage_of_config_change_commits",
        "percentage_of_merge_pr_commits",
        "percentage_of_unclassified_commits"
    )
    ordering = ("-repository",)
    search_fields = ["repository__name",]


@admin.register(CommitMessage)
class CommitMessageAdmin(admin.ModelAdmin):
    list_display = (
        "repository",
        "analyzed",
        "commit_hash",
        "author",
        "message",
        "commit_type",
        "commit_message_char_length",
        "words_amount",
        "average_word_length",
        "fog_index",
        "analyzed_time",
    )
    ordering = ("-analyzed_time",)
    search_fields = ["repository__name",]
