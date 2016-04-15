import os
from click.testing import CliRunner

from conftest import read_index

from morenines import application


def test_update_no_changes(data_dir, expected_dir):
    runner = CliRunner()
    result = runner.invoke(application.main, ['update', data_dir])

    assert result.exit_code == 0

    expected_output = u"Index is up-to-date (no new or missing files)\n"

    assert result.output == expected_output

    result_index = read_index(data_dir)

    expected_index = read_index(expected_dir)

    assert result_index == expected_index


def test_update_add(data_dir, expected_dir):
    runner = CliRunner()
    result = runner.invoke(application.main, ['update', '--add-new', data_dir])

    assert result.exit_code == 0

    result_index = read_index(data_dir)

    expected_index = read_index(expected_dir)

    assert result_index == expected_index


def test_update_remove(data_dir, expected_dir):
    runner = CliRunner()
    result = runner.invoke(application.main, ['update', '--remove-missing', data_dir])

    assert result.exit_code == 0

    result_index = read_index(data_dir)

    expected_index = read_index(expected_dir)

    assert result_index == expected_index
