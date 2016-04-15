import os
from click.testing import CliRunner

from morenines import application


def test_create(data_dir, expected_dir):
    runner = CliRunner()
    result = runner.invoke(application.main, ['create', data_dir])

    assert result.exit_code == 0

    # Prepare for checks
    result_index_path = os.path.join(data_dir, '.morenines', 'index')

    assert os.path.isfile(result_index_path)

    with open(result_index_path) as f:
        result_index = [line for line in f.readlines() if not line.startswith("date: ")]

    expected_index_path = os.path.join(expected_dir, '.morenines', 'index')

    with open(expected_index_path) as f:
        expected_index = f.readlines()

    assert result_index == expected_index


def test_create_empty(data_dir, expected_dir):
    runner = CliRunner()
    result = runner.invoke(application.main, ['create', data_dir])

    assert result.exit_code == 0

    # Prepare for checks
    result_index_path = os.path.join(data_dir, '.morenines', 'index')

    assert os.path.isfile(result_index_path)

    with open(result_index_path) as f:
        result_index = [line for line in f.readlines() if not line.startswith("date: ")]

    expected_index_path = os.path.join(expected_dir, '.morenines', 'index')

    with open(expected_index_path) as f:
        expected_index = f.readlines()

    assert result_index == expected_index


def test_create_with_existing_index(data_dir):
    runner = CliRunner()
    result = runner.invoke(application.main, ['create', data_dir])

    assert result.exit_code == 1

    expected_output_prefix = u"ERROR: Index file already exists:"

    starts_with_expected = result.output.startswith(expected_output_prefix)

    assert starts_with_expected == True
