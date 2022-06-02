import pytest

from fregepoc.analyzers.core import AnalyzerFactory
from fregepoc.analyzers.tests.ruby.constans import MOCKED_RUBY_FILES
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.factories import RepositoryFileFactory


@pytest.mark.django_db
class TestRubyAnalyzerEmpty:
    def test_count_loc(self, settings, dummy_repo):
        settings.DOWNLOAD_PATH = MOCKED_RUBY_FILES
        analyzers = AnalyzerFactory.make_analyzers(ProgrammingLanguages.RUBY)
        repo_file = RepositoryFileFactory(
            repository=dummy_repo,
            language=ProgrammingLanguages.RUBY,
            **{"repo_relative_file_path": "EmptyFile.rb"},
        )
        for analyzer in analyzers:
            actual = analyzer.analyze(repo_file)
            assert actual["lines_of_code"] == 0
            assert actual["token_count"] == 0
            assert actual["average_lines_of_code"] == 0
            assert actual["average_token_count"] == 0
            assert actual["average_cyclomatic_complexity"] == 0
            assert actual["average_parameter_count"] == 0