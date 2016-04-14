import os
import pytest
import shutil

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

@pytest.fixture
def expected_dir(request, module_dir):
    test_name = request.function.__name__

    dir_name = test_name + '-expected'

    return os.path.join(module_dir, dir_name)
