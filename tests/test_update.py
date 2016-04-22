import os
from click.testing import CliRunner

from conftest import tmp_chdir, mn_dirs_equal

from morenines import application


def test_update_no_changes(data_dir, expected_dir):
    """No difference between source and expected."""
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['update'])

    assert result.exit_code == 0

    expected_output = u"Index is up-to-date (no new or missing files)\n"

    assert result.output == expected_output

    assert mn_dirs_equal(data_dir, expected_dir) == True


def test_update_add(data_dir, expected_dir):
    """Adds a single new file to an index that doesn't have a parent"""
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['update', '--add-new'])

    assert result.exit_code == 0

    assert mn_dirs_equal(data_dir, expected_dir) == True


def test_update_add2(data_dir, expected_dir):
    """Adds a new file to an index that has a parent"""
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['update', '--add-new'])

    assert result.exit_code == 0

    assert mn_dirs_equal(data_dir, expected_dir) == True


def test_update_remove(data_dir, expected_dir):
    """Removes a file from an index that doesn't have a parent"""
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['update', '--remove-missing'])

    assert result.exit_code == 0

    assert mn_dirs_equal(data_dir, expected_dir) == True


def test_update_remove2(data_dir, expected_dir):
    """Removes a file from an index that has a parent"""
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['update', '--remove-missing'])

    assert result.exit_code == 0

    assert mn_dirs_equal(data_dir, expected_dir) == True
