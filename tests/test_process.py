from unittest.mock import patch
from earthquake_app.process import fetch_earthquakes_near_offices, fetch_earthquakes_custom_zone


@patch('earthquake_app.process.store_in_bigquery')
@patch('earthquake_app.process.fetch_earthquake_data')
@patch('earthquake_app.config.settings.get_settings')
def test_fetch_earthquakes_near_offices(mock_get_settings, mock_fetch_data, mock_store_in_bigquery):
    mock_get_settings.return_value.office_locations = [
        {"lat": 34.05, "lon": -118.25, "city": "Los Angeles"},
        {"lat": 37.77, "lon": -122.42, "city": "San Francisco"}
    ]
    mock_fetch_data.return_value = [
        {
            "date_time": "2024-09-15T00:00:00Z",
            "magnitude": 4.5,
            "latitude": 34.05,
            "longitude": -118.25,
            "place": "Los Angeles"
        }
    ]

    fetch_earthquakes_near_offices("2024-09-01", "2024-09-15", 100)

    mock_fetch_data.assert_called()
    mock_store_in_bigquery.assert_called()


@patch('earthquake_app.process.store_in_bigquery')
@patch('earthquake_app.process.fetch_earthquake_data')
def test_fetch_earthquakes_custom_zone(mock_fetch_data, mock_store_in_bigquery):
    mock_fetch_data.return_value = [
        {
            "date_time": "2024-09-15T00:00:00Z",
            "magnitude": 3.2,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "place": "New York"
        }
    ]

    fetch_earthquakes_custom_zone(40.7128, -74.0060, "2024-09-01", "2024-09-15", 50)

    mock_fetch_data.assert_called_once_with(40.7128, -74.0060, "2024-09-01", "2024-09-15", 50)
    mock_store_in_bigquery.assert_called_once()
