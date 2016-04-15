import os
from click.testing import CliRunner

from morenines import application


def test_update_add(data_dir, expected_dir):
    runner = CliRunner()
    result = runner.invoke(application.main, ['update', '--add-new', data_dir])

    # Prepare for checks
    result_index_path = os.path.join(data_dir, '.morenines', 'index')

    assert os.path.isfile(result_index_path)

    with open(result_index_path) as f:
        result_index = [line for line in f.readlines() if not line.startswith("date: ")]

    expected_index_path = os.path.join(expected_dir, '.morenines', 'index')

    with open(expected_index_path) as f:
        expected_index = f.readlines()

    assert result_index == expected_index
