




"""
These tests work on any integrations using BasicRest classes
"""

import json
import pytest
from jsonschema import validate
from .output_verify import OUTPUT_MAP
import functools
from unittest.mock import patch
from requests import Session
import pickle
from deepdiff import DeepDiff
import os
import sys
import re


# For shell execution
sys.path.append(os.getcwd())

# Globals
DATA_DIR = f'{os.getcwd()}/tests'

# Config Variables
STRICT_OUTPUT_KEYS = False  # Should output manifest have every key in response?
# Maybe we can't test test_1 certain task generically.
# todo: add data or these tasks.
TASKS_TO_SKIP = [
    'analyse_file',
    'analyse_url',
    'get_analyses',
    'reanalyse_file',
    'reanalyse_url',
    'get_augment_widget_url'
]


def get_task_names():
    tasks = [x.replace('.py', '') for x in os.listdir(f'{os.getcwd()}/imports') if x.endswith('.py')]
    # asset is its own test
    if 'asset' in tasks:
        tasks.remove('asset')
    # remove tasks to skip
    [tasks.remove(task) for task in TASKS_TO_SKIP]
    return tasks


def gather_test_dirs(task):
    return [d for d in os.listdir(f'{DATA_DIR}/{task}') if re.findall(r'test_.+', d)]


def gather_tests():
    tests = []
    for task in get_task_names():
        for test in gather_test_dirs(task):
            tests.append((task, test))
    return tests


def build_mock(mock_definitions):

    def mock_handler(self, *args, **kwargs):
        comparable = {
            #"headers": self.headers,
            "args": list(args),
            "kwargs": kwargs
        }
        #comparable['headers'].pop("User-Agent", None)
        for request in mock_definitions:
            if DeepDiff(comparable, request['request']) == {}:
                return pickle.loads(bytes.fromhex(request["response"]))
        else:
            raise (Exception(f"No mock found for request args: {args}, kwargs: {kwargs}"))

    return mock_handler


def mock_session(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args[0].mock_requests:
            with patch.object(Session, 'request', build_mock(args[0].mocks)):
                return func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper


@pytest.mark.parametrize("task, test", gather_tests())
class TestStandardRest:

    @mock_session
    @pytest.fixture(autouse=True)
    def _set_ctx(self, cls, task, test, mock_data, mock_requests):
        self.task = task
        self.test = test
        self.mocks = mock_data
        self.ctx = cls
        self.mock_requests = mock_requests

    def test_kwargs(self, *args, **kwargs):
        """
        This will test the payload schema json, params, data, files, etc. As utils passes it.
        """
        schema = json.loads(open(f'{DATA_DIR}/{self.task}/schemas/payload.json').read())
        validate(
            instance=self.ctx.get_kwargs(),
            schema=schema
        )

    def test_session_headers(self, test, *args, **kwargs):
        """
        Verify session headers against schema
        """
        schema = json.loads(open(f'{DATA_DIR}/{self.task}/schemas/headers.json').read())
        validate(
            instance=self.ctx.session.headers,
            schema=schema
        )

    @mock_session
    def test_parse_response(self, *args, **kwargs):
        """
        Execute task and verify data to output manifest types.
        """
        resp = self.ctx.execute()
        assert self.validate_output_manifest(resp)
        assert DeepDiff(resp, json.load(open(f'{DATA_DIR}/{self.task}/{self.test}/output.json'))) == {}

    def validate_output_manifest(self, resp, *args, **kwargs):
        """
        Helper function:
        Loads the task manifest and compares task results to output type schema.
        """
        missing = []  # store missing outputs
        schema = json.loads(open(f'imports/{self.task}.json').read())['availableOutputVariables']
        if isinstance(resp, dict):
            resp = [resp]
        for record in resp:
            for k, v in record.items():
                _type = schema.get(k, {}).get('type')
                # Todo handle all of the types in output_verify.py and rewrite this POC.
                if _type in [1, 6, 5, 9]:
                    if not OUTPUT_MAP[_type](v):
                        raise TypeError(f'Output Key: {k}, Type: {_type}\nValue: {v}')
                else:
                    missing.append(k)
        if STRICT_OUTPUT_KEYS and len(missing) > 0:
            raise Exception('Missing required outputs in task manifest')

        return True
