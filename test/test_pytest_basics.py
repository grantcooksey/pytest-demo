import os
import copy
from unittest import mock
import requests

from taxi_trips import sleep_demo

import pytest

# This statement is only used to make it easier to only run unit test modules.
# Integration test modules will have `pytestmark = pytest.mark.integration`
# Check out the `pytest.ini` to the list of other manually defined pytest marks
#
# Command to run unit tests: `pytest -m unit`
pytestmark = pytest.mark.unit


# pytest looks for functions prefixed with `test`
def test_basic():
    def add_2(x):
        return x + 2

    # use python standard assert to verify expectations
    assert add_2(5) == 7

    # Can use multiple assertions in the same test
    assert add_2(1) == 3


# functions that aren't prefixed with test are ignored
def i_am_ignored():
    pass


# assert that an exception is raised
def test_raise_exception():
    def divide_by_zero():
        5 / 0

    with pytest.raises(ZeroDivisionError):
        divide_by_zero()


@pytest.mark.skip
def test_will_fail():
    assert False


# fixtures provide a dependable baseline to set up test data
@pytest.fixture
def env_var_config():
    return {
        'YEAR': '2019'
    }


# project code would call get_year_env_var()
def get_year_env_var(config=os.environ):
    return config['YEAR']


# Test functions can receive fixture objects by naming them as an input argument
def test_get_year_env_var(env_var_config):
    assert get_year_env_var(config=env_var_config) == '2019'


# fixtures are modular and can use other fixtures
@pytest.fixture
def plus_one_year_env_config(env_var_config):
    new_config = copy.copy(env_var_config)
    new_config['YEAR'] = str(int(new_config['YEAR']) + 1)
    return new_config


def test_get_year_env_var_plus_one(plus_one_year_env_config, env_var_config):
    assert get_year_env_var(config=plus_one_year_env_config) == '2020'


# fixtures cover setup, but what about tear down?
@pytest.fixture
def tear_down():
    print('I am called before the test')
    yield 'the test'
    print('I am called after the test')


def test_tear_down(tear_down):
    print(tear_down)


# mock object substitutes and imitates a real object within a testing environment
def test_mock():
    mocked_object = mock.MagicMock()
    mocked_object.some_function(this_is_a_parameter=5)
    mocked_object.some_function.assert_called_once_with(this_is_a_parameter=5)


# You don't want to reach out to external systems during a unit test
def test_dont_hit_google():
    mocked_request = mock.MagicMock()
    mocked_response = mock.MagicMock()
    mocked_request.get.return_value = mocked_response  # mock function
    mocked_response.status_code = 200  # mock property

    def get_google_response_status_code(request_service=requests):
        response = request_service.get('https://google.com')
        return response.status_code

    assert get_google_response_status_code(request_service=mocked_request) == 200


# but what if we can't access the internal function? We can patch it using pytest-mock
def test_dont_hit_google_with_patching(mocker):
    mocked_response = mock.MagicMock()
    mocked_response.status_code = 200  # mock property
    mocker.patch.object(requests, 'get', return_value=mocked_response)

    def get_google_response_status_code():
        response = requests.get('https://google.com')
        return response.status_code

    assert get_google_response_status_code() == 200


# dont want to sleep in our unit tests so they run fast
@pytest.fixture(autouse=True)
def no_sleep_tonight(mocker):
    mocker.patch.object(sleep_demo.time, 'sleep')


def test_sleep_demo():
    assert sleep_demo.long_sleep()
