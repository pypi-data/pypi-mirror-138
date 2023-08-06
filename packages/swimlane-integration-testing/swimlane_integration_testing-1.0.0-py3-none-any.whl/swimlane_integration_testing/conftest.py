import json
import pytest
import os
import importlib

DATA_DIR = f'{os.getcwd()}/tests'


def sw_main(task, _inputs, _asset):
    mod = importlib.import_module(f'imports.{task}')
    if not _asset:
        _asset = json.loads(open(f'{DATA_DIR}/asset/asset.json').read())

    class Context:
        asset = _asset
        inputs = _inputs
    ctx = mod.SwMain(Context)
    return ctx


@pytest.fixture
def cls(task, test):
    """Instantiate SwMain for general tests"""
    inputs = json.load(open(f'{DATA_DIR}/{task}/{test}/inputs.json')) if task != 'asset' else {}
    return sw_main(task, inputs, None)


@pytest.fixture
def mock_data(task, test):
    """
    Get the mock data for the test
    """
    file_path = f'{DATA_DIR}/{task}/{test}/mocks.json'
    mocks = []
    if os.path.exists(file_path):
        mocks = json.load(open(f'{DATA_DIR}/{task}/{test}/mocks.json', 'r'))
    return mocks


@pytest.fixture
def mock_requests(pytestconfig):
    return pytestconfig.getoption("mock")


def pytest_addoption(parser):
    parser.addoption("--mock",
                     help='Use mock requests defined in "mocks.json" for all default tests.',
                     action="store_true",
                     default=False)


