from unittest import mock
from taxi_trips import passenger_count

import pytest
pytestmark = pytest.mark.integration


@pytest.fixture
def test_data_path(tmp_path, mocker):
    mocker.patch.object(passenger_count, 'RESULT_PATH')
    data_dir = tmp_path / 'data'
    data_dir.mkdir()
    passenger_count.RESULT_PATH = str(data_dir) + '/'
    return data_dir


# data report is huge so we don't want to pull it in a test
# Lets test the load side, verify that given a report,
# it shows up how we expect in the filesystem
def test_integration(test_data_path, config, raw_ten_passenger_taxi_records):
    mock_response = mock.MagicMock()
    mock_response.text = raw_ten_passenger_taxi_records
    passenger_count.requests.get.return_value = mock_response

    passenger_count.start_job(config=config)

    data_file = test_data_path / '2018_01_count_passengers.csv'
    assert data_file.read_text() == 'passenger_count\n10\n'
