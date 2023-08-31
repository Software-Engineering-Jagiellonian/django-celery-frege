from rest_framework import serializers

from fregepoc.repositories.models import Repository, RepositoryFile, CommitMessage, RepositoryCommitMessagesQuality


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = [
            "id",
            "description",
            "analyzed",
            "git_url",
            "repo_url",
            "commit_hash",
            "discovered_time",
            "fetch_time",
        ]


class RepositoryFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepositoryFile
        fields = [
            "id",
            "repository",
            "analyzed",
            "language",
            "repo_relative_file_path",
            "metrics",
            "analyzed_time",
        ]


class CommitMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitMessage
        fields = [
            "id",
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
        ]


class RepositoryCommitMessagesQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RepositoryCommitMessagesQuality
        fields = [
            "id",
            "repository",
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
        ]
