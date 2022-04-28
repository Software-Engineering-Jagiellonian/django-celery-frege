from rest_framework import serializers

from fregepoc.repositories.models import Repository, RepositoryFile


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ['id', 'description', 'analyzed', 'git_url', 'repo_url', 'commit_hash', 'discovered_time',
                  'fetch_time']


class RepositoryFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepositoryFile
        fields = ['id', 'repository', 'analyzed', 'language', 'repo_relative_file_path', 'metrics', 'analyzed_time']
