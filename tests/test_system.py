import os
import pytest
import shutil
import click
from click.testing import CliRunner

from morenines import application


@pytest.fixture
def module_dir(request):
    mod_file = request.module.__file__
    module_dir , _ = os.path.splitext(mod_file)

    return module_dir


@pytest.fixture
def data_dir(request, tmpdir, module_dir):
    test_name = request.function.__name__

    source_path = os.path.join(module_dir, test_name)

    dest_path = tmpdir.join(test_name)

    shutil.copytree(source_path, dest_path.strpath)

    return dest_path.strpath


def test_init(data_dir):
    runner = CliRunner()

    result = runner.invoke(application.main, ['init', data_dir])

    mn_dir = os.path.join(data_dir, '.morenines')

    assert os.path.isdir(mn_dir) == True


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
