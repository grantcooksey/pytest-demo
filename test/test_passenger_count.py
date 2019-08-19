import io
import copy
from collections.abc import Iterable
from unittest import mock
from requests.exceptions import ConnectTimeout
from taxi_trips import passenger_count

import pytest
pytestmark = pytest.mark.unit


@pytest.fixture(autouse=True)
def patch_request_get(mocker):
    mocker.patch.object(passenger_count.requests, 'get')


@pytest.fixture
def config():
    return {
        'YEAR': '2018',
        'MONTH': '01'
    }


@pytest.fixture
def ten_person_taxi_report_file(raw_ten_passenger_taxi_records):
    return io.StringIO(raw_ten_passenger_taxi_records)


def test_pull_file_returns_buffer(config, raw_ten_passenger_taxi_records):
    mock_response = mock.MagicMock()
    mock_response.text = raw_ten_passenger_taxi_records

    passenger_count.requests.get.return_value = mock_response
    file = passenger_count.pull_file(year=config['YEAR'], month=['MONTH'])

    assert isinstance(file, Iterable)


def test_pull_file_errors_on_timeout(config):
    def timeout(url, allow_redirects, timeout):
        raise ConnectTimeout('Too slow!')

    # Use side effects when you need to do more than return a value, like raise an exception
    passenger_count.requests.get.side_effect = timeout
    with pytest.raises(ConnectTimeout):
        passenger_count.pull_file(year=config['YEAR'], month=['MONTH'])


def test_pull_file_errors_on_non_successful_response(config):
    class MockSuccessResponse:
        def raise_for_status(self):
            raise Exception('404!')

    passenger_count.requests.get.return_value = MockSuccessResponse
    with pytest.raises(Exception):
        passenger_count.pull_file(year=config['YEAR'], month=['MONTH'])


def test_count_people(ten_person_taxi_report_file):
    assert passenger_count.count_people(ten_person_taxi_report_file) == 10


def test_count_people_handles_empty_file():
    assert passenger_count.count_people(io.StringIO('')) == 0
