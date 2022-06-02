import pytest

from fregepoc.analyzers.core import AnalyzerFactory
from fregepoc.analyzers.tests.ruby.constans import MOCKED_RUBY_FILES
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.factories import RepositoryFileFactory


@pytest.mark.django_db
class TestRubyAnalyzerAverageCount:
    @pytest.mark.parametrize(
        ["repo_file_params", "expected_average_parameter_count"],
        [
            (
                {"repo_relative_file_path": "data_mapper.rb"},
                0.0,
            ),
            (
                {"repo_relative_file_path": "file_read.rb"},
                1.2,
            ),
            (
                {"repo_relative_file_path": "expand_path.rb"},
                1.3,
            ),
        ],
    )
    def test_count_loc(
        self,
        repo_file_params,
        expected_average_parameter_count,
        settings,
        dummy_repo,
    ):
        settings.DOWNLOAD_PATH = MOCKED_RUBY_FILES
        analyzers = AnalyzerFactory.make_analyzers(ProgrammingLanguages.RUBY)
        repo_file = RepositoryFileFactory(
            repository=dummy_repo,
            language=ProgrammingLanguages.RUBY,
            **repo_file_params,
        )
        for analyzer in analyzers:
            actual = analyzer.analyze(repo_file)
            assert actual["average_parameter_count"] == pytest.approx(
                expected_average_parameter_count, 0.01
            )