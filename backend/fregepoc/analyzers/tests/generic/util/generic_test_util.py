import pytest

from fregepoc.analyzers.core import AnalyzerFactory
from fregepoc.repositories.factories import RepositoryFileFactory


def generic_test(
    repo_file_params,
    expected_values,
    settings,
    dummy_repo,
    mocked_files_path,
    programming_language,
    parameter_types,
):
    settings.DOWNLOAD_PATH = mocked_files_path
    analyzers = AnalyzerFactory.make_analyzers(programming_language)
    repo_file = RepositoryFileFactory(
        repository=dummy_repo,
        language=programming_language,
        **repo_file_params,
    )
    for analyzer in analyzers:
        actual = analyzer.analyze(repo_file)
        for (param, expected) in zip(parameter_types, expected_values):
            error_message = (
                f"actual: {actual[param]} not equal to expected: {expected}"
            )
            assert actual[param] == pytest.approx(
                expected, 0.01
            ), error_message
