import json
import pytest
import data_processing

# defining fixtures
@pytest.fixture
def data_proc():
    data_proc = data_processing.DataProcessor("2020-11-11")
    return data_proc

# loading json response for mock
@pytest.fixture()
def mock_api_response():
    with open("payload.json") as file:
        return json.load(file)

# testing delta increase
def test_increase_delta_by_one_valid(data_proc):
    data_proc.increase_delta_by_one()
    assert data_proc.delta == 2

# testing date change mechanism
def test_day_before_transaction_valid(data_proc):
    new_date = data_proc.day_before_transaction()
    assert new_date == "2020-11-10"

# testing main function with mocker
def test_get_data_from_nbp_valid(mocker, mock_api_response, data_proc):
    mock_response = mocker.Mock()
    mock_response.json = mocker.Mock(return_value=mock_api_response)
    mock_response.status_code = 200
    mocker.patch("data_processing.DataProcessor.api_call_to_nbp", return_value=mock_response)

    usd_fx_rate = data_proc.get_data_from_nbp()
    assert usd_fx_rate == 3.8168