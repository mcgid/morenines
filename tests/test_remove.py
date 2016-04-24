import os
from click.testing import CliRunner

from conftest import tmp_chdir, assert_mn_dirs_equal

from morenines import application


def test_remove_no_changes(data_dir, expected_dir):
    """No difference between source and expected."""
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['remove'])

    assert result.exit_code == 0

    expected_output = u"WARNING: No action taken (supply one or more PATHS to files to add to the repository)\n"

    assert result.output == expected_output

    assert_mn_dirs_equal(data_dir, expected_dir)


def test_remove(data_dir, expected_dir):
    """Removes a file from an index that doesn't have a parent"""
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['remove', '2012/file_to_del.txt'])

    assert result.exit_code == 0

    assert_mn_dirs_equal(data_dir, expected_dir)


def test_remove2(data_dir, expected_dir):
    """Removes a file from an index that has a parent"""
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['remove', 'file_to_del2.txt'])

    assert result.exit_code == 0

    assert_mn_dirs_equal(data_dir, expected_dir)


def test_remove_path_outside_repo(data_dir, expected_dir):
    """Tries to remove a path outside of the repository"""
    bad_abs_path = os.path.join(os.path.dirname(data_dir), "fake_file.txt")

    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['remove', bad_abs_path])

    assert result.exit_code == 1

    assert_mn_dirs_equal(data_dir, expected_dir)


def test_remove_multiple(data_dir, expected_dir):
    """Removes multiple paths at the same time"""
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['remove', '2012/file_to_del.txt', 'file_to_del2.txt'])

    assert result.exit_code == 0

    assert_mn_dirs_equal(data_dir, expected_dir)

def test_remove_missing_arg(data_dir, expected_dir):
    """Tries to remove without specifying a path to remove"""
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['remove'])

    assert result.exit_code == 0

    expected_output = u"WARNING: No action taken (supply one or more PATHS to files to add to the repository)\n"

    assert result.output == expected_output

    assert_mn_dirs_equal(data_dir, expected_dir)
