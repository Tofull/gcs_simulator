import pathlib
import pytest


@pytest.fixture
def data_directory():
    tests_directory = pathlib.Path(__file__).parent
    DATA_PATH = tests_directory / ".." / "data"
    return DATA_PATH.resolve().absolute()
