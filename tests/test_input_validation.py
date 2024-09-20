# pylint: disable=redefined-outer-name

import pytest
from earthquake_app.core.utils import (
    validate_latitude,
    validate_longitude,
    validate_radius,
    validate_dates,
    InputValidationError,
)


@pytest.fixture
def valid_lat_lon_data():
    return 45.0, 90.0  # valid latitude and longitude


@pytest.fixture
def invalid_lat_lon_data():
    return [100.0, 200.0]  # invalid latitude and longitude


@pytest.fixture
def valid_dates_data():
    return "2023-01-01", "2023-12-31"  # valid start and end dates


@pytest.fixture
def invalid_dates_data():
    return [
        ("2023-12-31", "2023-01-01"),  # start after end
        ("2023/01/01", "2023-12-31"),  # invalid date format
        ("2023-01-01", "31-12-2023"),  # invalid date format
    ]


@pytest.fixture
def valid_radius_value():
    return 500.0  # valid radius


@pytest.fixture
def invalid_radius_values():
    return [-10.0, 30000.0]  # invalid radii


def test_validate_lat_lon(valid_lat_lon_data, invalid_lat_lon_data):
    lat, lon = valid_lat_lon_data
    validate_latitude(lat)  # should pass
    validate_longitude(lon)  # should pass

    for invalid_lat in invalid_lat_lon_data:
        if invalid_lat == 100.0:
            with pytest.raises(
                InputValidationError, match="Latitude must be between -90.0 and 90.0 degrees."
            ):
                validate_latitude(invalid_lat)
        else:
            with pytest.raises(
                InputValidationError, match="Longitude must be between -180.0 and 180.0 degrees."
            ):
                validate_longitude(invalid_lat)


def test_validate_radius(valid_radius_value, invalid_radius_values):
    validate_radius(valid_radius_value)  # should pass

    for radius in invalid_radius_values:
        with pytest.raises(InputValidationError, match="Radius must be between 0 and 20001.6 km."):
            validate_radius(radius)  # should fail


def test_validate_dates(valid_dates_data, invalid_dates_data):
    start_time, end_time = valid_dates_data
    validate_dates(start_time, end_time)  # should pass

    for start, end in invalid_dates_data:
        if start == "2023-12-31" and end == "2023-01-01":
            with pytest.raises(
                InputValidationError, match="Start time must be less than end_time."
            ):
                validate_dates(start, end)  # should fail
        else:
            with pytest.raises(
                InputValidationError, match=f"{start}|{end} is not a valid ISO8601 format."
            ):
                validate_dates(start, end)  # should fail
