import os
from click.testing import CliRunner

from conftest import read_index

from morenines import application


def test_create(data_dir, expected_dir):
    runner = CliRunner()
    result = runner.invoke(application.main, ['create', data_dir])

    assert result.exit_code == 0

    result_index = read_index(data_dir)

    expected_index = read_index(expected_dir)

    assert result_index == expected_index


def test_create_empty(data_dir, expected_dir):
    runner = CliRunner()
    result = runner.invoke(application.main, ['create', data_dir])

    assert result.exit_code == 0

    result_index = read_index(data_dir)

    expected_index = read_index(expected_dir)

    assert result_index == expected_index


def test_create_with_existing_index(data_dir):
    runner = CliRunner()
    result = runner.invoke(application.main, ['create', data_dir])

    assert result.exit_code == 1

    expected_output_prefix = u"ERROR: Index file already exists:"

    starts_with_expected = result.output.startswith(expected_output_prefix)

    assert starts_with_expected == True
