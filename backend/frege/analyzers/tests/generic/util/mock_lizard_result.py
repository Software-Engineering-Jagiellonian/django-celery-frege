from unittest.mock import MagicMock


def mock_lizard_result(nloc=0,token_count=0,average_nloc=0,average_token_count=0,average_cyclomatic_complexity=0,average_parameter_count=0):
    """Create a mock lizard analysis result."""
    mock_result = MagicMock()
    mock_result.nloc = nloc
    mock_result.token_count = token_count
    mock_result.average_nloc = average_nloc
    mock_result.average_token_count = average_token_count
    mock_result.average_cyclomatic_complexity = average_cyclomatic_complexity
    mock_result.functions_average.return_value = average_parameter_count
    mock_result.function_list = [
        MagicMock(name="moc_func1"),
        MagicMock(name="moc_func2"),
    ]
    for i in range(len(mock_result.function_list)):
        mock_result.function_list[i].name = f"func{i}"
    return mock_result
