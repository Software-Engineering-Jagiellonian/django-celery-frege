from unittest import TestCase
from unittest.mock import patch
from pathlib import Path
from django.conf import settings
from frege.repositories import models
from frege.repositories.utils.analyzers import repo_file_content
from frege.repositories.utils.paths import (
    get_repo_local_path,
    get_repo_files,
    get_file_abs_path
)
from unittest.mock import MagicMock
from frege.repositories.constants import ProgrammingLanguages

class GetRepoLocalPathTests(TestCase):
    @patch.object(settings, "DOWNLOAD_PATH", "/fake/path")
    def test_get_repo_local_path(self):
        repo = models.Repository(pk=123)
        expected_path = Path("/fake/path/123")
        self.assertEqual(get_repo_local_path(repo), expected_path)

class GetRepoFilesTests(TestCase):
    def test_get_repo_files(self):
        mock_repo = MagicMock()
        mock_repo.git.ls_files.return_value = "file1.py\nfile2.go\nfile3.txt"

        expected_output = [
            ("file1.py", ProgrammingLanguages.PYTHON),
            ("file2.go", ProgrammingLanguages.GOLANG),
        ]

        with patch("frege.repositories.constants.get_languages_by_extension") as mock_lang:
            mock_lang.side_effect = lambda ext: (
                [ProgrammingLanguages.PYTHON] if ext == ".py" else
                [ProgrammingLanguages.GOLANG] if ext == ".go" else []
            )

            result = list(get_repo_files(mock_repo))
            self.assertEqual(result, expected_output)

class GetFileAbsPathTests(TestCase):
    @patch("frege.repositories.utils.paths.get_repo_local_path")
    def test_get_file_abs_path(self, mock_get_repo_local_path):
        mock_get_repo_local_path.return_value = Path("/fake/repo/path")

        repo_file = MagicMock()
        repo_file.repository = MagicMock()
        repo_file.repo_relative_file_path = "src/main.py"

        expected_path = Path("/fake/repo/path/src/main.py")
        self.assertEqual(get_file_abs_path(repo_file), expected_path)