import os
from click.testing import CliRunner

from conftest import tmp_chdir

from morenines import application


def test_status_no_changes_with_color(data_dir):
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['status'])

    assert result.exit_code == 0

    expected_output = u"\033[32mIndex is up-to-date (no changes)\n\033[0m"

    assert result.output == expected_output


def test_status_no_changes_no_color(data_dir):
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['status', '--no-color'])

    assert result.exit_code == 0

    expected_output = u"Index is up-to-date (no changes)\n"

    assert result.output == expected_output


def test_status_new_file_with_color(data_dir):
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['status'])

    assert result.exit_code == 0

    # Result output is unicode, so we need a unicode string literal
    expected_output = u"\033[33mNew files (not in index):\n  2012/new_file.txt\n\033[0m"

    assert result.output == expected_output


def test_status_new_file_no_color(data_dir):
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['status', '--no-color'])

    assert result.exit_code == 0

    # Result output is unicode, so we need a unicode string literal
    expected_output = u"New files (not in index):\n  2012/new_file.txt\n"

    assert result.output == expected_output


def test_status_missing_file_with_color(data_dir):
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['status'])

    assert result.exit_code == 0

    # Result output is unicode, so we need a unicode string literal
    expected_output = u"\033[33mMissing files:\n  2012/file_to_del.txt\n\033[0m"

    assert result.output == expected_output


def test_status_missing_file_no_color(data_dir):
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['status', '--no-color'])

    assert result.exit_code == 0

    # Result output is unicode, so we need a unicode string literal
    expected_output = u"Missing files:\n  2012/file_to_del.txt\n"

    assert result.output == expected_output


def test_status_ignored_file_with_color(data_dir):
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['status', '--ignored'])

    assert result.exit_code == 0

    # Result output is unicode, so we need a unicode string literal
    expected_output = u"\033[34mIgnored files and directories:\n  .morenines/\n  2012/file_to_ignore.txt\n\033[0m"

    assert result.output == expected_output


def test_status_ignored_file_no_color(data_dir):
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['status', '--ignored', '--no-color'])

    assert result.exit_code == 0

    # Result output is unicode, so we need a unicode string literal
    expected_output = u"Ignored files and directories:\n  .morenines/\n  2012/file_to_ignore.txt\n"

    assert result.output == expected_output


def test_status_changed_file_with_color(data_dir):
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['status', '--verify'])

    assert result.exit_code == 0

    # Result output is unicode, so we need a unicode string literal
    expected_output = u"\033[31mChanged files (hash differs from index):\n  2012/file_to_change.txt\n\033[0m"

    assert result.output == expected_output


def test_status_changed_file_no_color(data_dir):
    with tmp_chdir(data_dir):
        runner = CliRunner()
        result = runner.invoke(application.main, ['status', '--verify', '--no-color'])

    assert result.exit_code == 0

    # Result output is unicode, so we need a unicode string literal
    expected_output = u"Changed files (hash differs from index):\n  2012/file_to_change.txt\n"

    assert result.output == expected_output
