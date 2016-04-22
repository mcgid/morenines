import os
import pytest
import shutil
import contextlib

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


@contextlib.contextmanager
def tmp_chdir(path):
    cwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(cwd)


def read_file(path):
    assert os.path.isfile(path) == True

    with open(path, 'r') as f:
        # Kind of a hack but the date is always going to be different
        return [line for line in f.readlines() if not line.startswith("date: ")]


def files_equal(test_path, expected_path):
    test_file = read_file(test_path)

    expected_file = read_file(expected_path)

    return test_file == expected_file


def mn_dirs_equal(test_dir, expected):
    for parent_path, subdir_names, file_names in os.walk(expected):
        for file_name in file_names:
            expected_path = os.path.join(parent_path, file_name)

            rel_path = os.path.relpath(expected_path, expected)

            test_path = os.path.join(test_dir, rel_path)

            if not files_equal(test_path, expected_path):
                return False

        for subdir_name in subdir_names:
            subdir_path = os.path.join(parent_path, subdir_name)

            if not os.path.isdir(subdir_path):
                return False

    return True
