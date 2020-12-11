import pathlib
import shutil

import pytest


@pytest.fixture
def data_directory():
    tests_directory = pathlib.Path(__file__).parent
    DATA_PATH = tests_directory / ".." / "data"
    return DATA_PATH.resolve().absolute()


@pytest.fixture
def get_simple_txt_file(data_directory):
    txt_file = data_directory / "simple_txt_file.txt"

    return txt_file


@pytest.fixture
def empty_bucket_structure(tmpdir_factory):
    root_folder = tmpdir_factory.mktemp("cloud_storage_simulator")
    source_bucket_folder = root_folder.mkdir("bucket_source")
    destination_bucket_folder = root_folder.mkdir("bucket_destination")

    yield (str(root_folder), str(source_bucket_folder), str(destination_bucket_folder))

    shutil.rmtree(str(root_folder))


@pytest.fixture
def default_bucket_structure(empty_bucket_structure, get_simple_txt_file):
    (
        root_folder,
        source_bucket_folder,
        destination_bucket_folder,
    ) = empty_bucket_structure

    shutil.copy(get_simple_txt_file, source_bucket_folder)

    return (root_folder, source_bucket_folder, destination_bucket_folder)
