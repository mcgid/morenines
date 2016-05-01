import os
from click.testing import CliRunner

from conftest import tmp_chdir, assert_mn_dirs_equal

from morenines import application


def test_add_no_changes(data_dir, expected_dir):
    """No difference between source and expected."""
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['add'])

    assert result.exit_code == 0

    expected_output = u"WARNING: No action taken (supply one or more PATHS to files to add to the repository)\n"

    assert result.output == expected_output

    assert_mn_dirs_equal(data_dir, expected_dir)


def test_add(data_dir, expected_dir):
    """Adds a single new file to an index that doesn't have a parent"""
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['add', '2012/new_file.txt'])

    assert result.exit_code == 0

    assert_mn_dirs_equal(data_dir, expected_dir)


def test_add2(data_dir, expected_dir):
    """Adds a new file to an index that has a parent"""
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['add', 'new_file2.txt'])

    assert result.exit_code == 0

    assert_mn_dirs_equal(data_dir, expected_dir)

def test_add_path_outside_repo(data_dir, expected_dir):
    """Tries to add a path outside of the repository"""
    bad_abs_path = os.path.join(os.path.dirname(data_dir), "fake_file.txt")

    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['add', bad_abs_path])

    assert result.exit_code == 1

    assert_mn_dirs_equal(data_dir, expected_dir)


def test_add_multiple(data_dir, expected_dir):
    """Adds a single new file to an index that doesn't have a parent"""
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['add', '2012/new_file.txt', 'new_file2.txt'])

    assert result.exit_code == 0

    assert_mn_dirs_equal(data_dir, expected_dir)


def test_add_missing_arg(data_dir, expected_dir):
    """Tries to add without specifying path to add"""
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['add'])

    assert result.exit_code == 0

    expected_output = u"WARNING: No action taken (supply one or more PATHS to files to add to the repository)\n"

    assert result.output == expected_output

    assert_mn_dirs_equal(data_dir, expected_dir)


def test_add_dir(data_dir, expected_dir):
    """Tries to add a directory with a file in it"""
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['add', '2012/new_dir'])

    assert result.exit_code == 0

    assert_mn_dirs_equal(data_dir, expected_dir)
