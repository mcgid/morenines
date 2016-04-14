import os
from click.testing import CliRunner

from morenines import application


def test_init(data_dir):
    runner = CliRunner()

    result = runner.invoke(application.main, ['init', data_dir])

    mn_dir = os.path.join(data_dir, '.morenines')

    assert os.path.isdir(mn_dir) == True
