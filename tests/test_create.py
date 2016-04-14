import os
from click.testing import CliRunner

from morenines import application


def test_create(module_dir, data_dir):
    runner = CliRunner()
    result = runner.invoke(application.main, ['create', data_dir])

    # Prepare for checks
    result_index_path = os.path.join(data_dir, '.morenines', 'index')

    assert os.path.isfile(result_index_path)

    with open(result_index_path) as f:
        result_index = [line for line in f.readlines() if not line.startswith("date: ")]

    premade_index_path = os.path.join(module_dir, "index-after_create")

    with open(premade_index_path) as f:
        premade_index = f.readlines()

    assert result_index == premade_index
