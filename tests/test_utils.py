from unittest.mock import patch, MagicMock
import pytest
from earthquake_app.core.utils import fetch_earthquake_data, store_in_bigquery


@patch("earthquake_app.core.utils.USGSClient.request")
def test_fetch_earthquake_data_success(mock_request):
    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.json.return_value = {
        "features": [
            {
                "properties": {"time": "2024-09-15T00:00:00Z", "mag": 4.5, "place": "Los Angeles"},
                "geometry": {"coordinates": [-118.25, 34.05]},
            }
        ]
    }
    mock_request.return_value = mock_response

    data = fetch_earthquake_data(34.05, -118.25, "2024-09-01", "2024-09-15", 100.0)

    assert len(data) == 1
    assert data[0]["place"] == "Los Angeles"


@patch("earthquake_app.core.utils.USGSClient.request")
def test_fetch_earthquake_data_failure(mock_request):
    mock_response = MagicMock()
    mock_response.ok = False
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_request.return_value = mock_response

    with pytest.raises(Exception, match=r"API request failed with status code 500"):
        fetch_earthquake_data(34.05, -118.25, "2024-09-01", "2024-09-15", 100.0)


@patch("earthquake_app.core.utils.bigquery.Client")
def test_store_in_bigquery_success(mock_bigquery_client):
    # Mock settings and BigQuery client

    # Mock the BigQuery client's insert_rows_json method to return an empty list (success)
    mock_client_instance = mock_bigquery_client.return_value
    mock_client_instance.insert_rows_json.return_value = []

    # Call the function
    store_in_bigquery([{"data": "test_data"}])

    # Ensure insert_rows_json is called once
    mock_client_instance.insert_rows_json.assert_called_once()


@patch("earthquake_app.core.utils.bigquery.Client")
def test_store_in_bigquery_failure(mock_bigquery_client, caplog):
    # Mock the BigQuery client's insert_rows_json method to simulate an error
    mock_client_instance = mock_bigquery_client.return_value
    mock_client_instance.insert_rows_json.return_value = [{"errors": "Some error"}]

    # Call the function (it will use the real settings)
    store_in_bigquery([{"data": "test_data"}])

    # Ensure insert_rows_json is called once
    mock_client_instance.insert_rows_json.assert_called_once()

    # Check if an error was logged
    assert "BigQuery datastore encountered errors" in caplog.text
