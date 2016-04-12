import os
import pytest
import shutil
import click
from click.testing import CliRunner

from morenines import application


@pytest.fixture
def test_dir(request):
    mod_file = request.module.__file__
    test_dir , _ = os.path.splitext(mod_file)

    return test_dir


@pytest.fixture
def example_dir(test_dir, tmpdir):
    dest_path = tmpdir.join(os.path.basename(test_dir))

    data_dir = os.path.join(test_dir, "data0")

    shutil.copytree(data_dir, dest_path.strpath)

    return dest_path.strpath
    

def test_init(example_dir):
    runner = CliRunner()

    result = runner.invoke(application.main, ['init', example_dir])

    mn_dir = os.path.join(example_dir, '.morenines')

    assert os.path.isdir(mn_dir) == True


def test_create(test_dir, example_dir):
    # Prepare the environment
    result_mn_dir = os.path.join(example_dir, ".morenines")
    os.mkdir(result_mn_dir)

    # Run it
    runner = CliRunner()
    result = runner.invoke(application.main, ['create', example_dir])

    # Prepare for checks
    result_index_path = os.path.join(result_mn_dir, 'index')

    assert os.path.isfile(result_index_path)

    with open(result_index_path) as f:
        result_index = [line for line in f.readlines() if not line.startswith("date: ")]


    premade_index_path = os.path.join(test_dir, "index-after_create")

    with open(premade_index_path) as f:
        premade_index = f.readlines()

    assert result_index == premade_index
