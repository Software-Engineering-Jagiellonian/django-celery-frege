from unittest.mock import call

import pytest
from pytest_mock import MockerFixture

from fregepoc.repositories.models import RepositoryFile
from fregepoc.repositories.tasks import process_repo_task
from fregepoc.repositories.utils.paths import get_repo_local_path
from fregepoc.repositories.utils.tests import MOCK_DOWNLOAD_PATH


@pytest.mark.django_db
class TestProcessRepoTask:
    def test_process_repo_task(self, mocker: MockerFixture, dummy_repo, settings):
        settings.DOWNLOAD_PATH = MOCK_DOWNLOAD_PATH
        analyze_file_task_mock = mocker.MagicMock()
        clone_from_mock = mocker.MagicMock()
        repo_obj_mock = mocker.MagicMock()
        repo_obj_mock.git.ls_files = lambda: "ans.cpp\nhello_world.py"
        clone_from_mock.return_value = repo_obj_mock
        mocker.patch(
            "fregepoc.repositories.tasks.analyze_file_task.delay",
            analyze_file_task_mock,
        )
        mocker.patch("fregepoc.repositories.tasks.logger")
        mocker.patch("git.repo.base.Repo.clone_from", clone_from_mock)
        process_repo_task.run(dummy_repo.pk)
        clone_from_mock.assert_called_once_with(
            dummy_repo.git_url, get_repo_local_path(dummy_repo)
        )
        assert RepositoryFile.objects.filter(repository=dummy_repo).count() == 2
        for repo_file in dummy_repo.files.all():
            analyze_file_task_mock.assert_has_calls([call(repo_file.pk)])
