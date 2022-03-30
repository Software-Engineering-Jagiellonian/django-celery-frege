import pytest

from fregepoc.repositories.analyzers.base import AnalyzerFactory
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.models import RepositoryFile
from fregepoc.repositories.utils.tests import MOCK_DOWNLOAD_PATH


@pytest.mark.django_db
class TestCppAnalyzers:
    def test_analyzers_makes_some_analysis(self, settings, dummy_repo):
        settings.DOWNLOAD_PATH = MOCK_DOWNLOAD_PATH
        analyzers = AnalyzerFactory.make_analyzers(ProgrammingLanguages.CPP)
        repo_file = RepositoryFile(
            repository=dummy_repo,
            repo_relative_file_path="ans.cpp",
            language=ProgrammingLanguages.CPP,
        )
        for analyzer in analyzers:
            result_dict = analyzer.analyze(repo_file)
            assert result_dict
