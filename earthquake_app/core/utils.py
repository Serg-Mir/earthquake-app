from datetime import datetime
from decimal import Decimal

import logging
from google.cloud import bigquery
from earthquake_app.config.settings import get_settings
from earthquake_app.core.clients import USGSClient
from earthquake_app.core.exceptions import APIRequestError, InputValidationError


logger = logging.getLogger("earthquake_app.utils")


def fetch_earthquake_data(
    lat: float, lon: float, start_time: str, end_time: str, radius: float
) -> list[dict]:
    client = USGSClient()
    params = {
        "format": "geojson",
        "starttime": start_time,
        "endtime": end_time,
        "latitude": lat,
        "longitude": lon,
        "maxradiuskm": radius,
    }

    response = client.request("GET", params=params)

    # We might prefer to have response.raise_for_status() here but I left it for better error handling
    if response.ok:
        logger.debug("Successful data retrieval from API")
        data = response.json()
        rows_to_insert = [
            {
                "date_time": earthquake["properties"]["time"],
                "magnitude": earthquake["properties"]["mag"],
                "latitude": earthquake["geometry"]["coordinates"][1],
                "longitude": earthquake["geometry"]["coordinates"][0],
                "place": earthquake["properties"]["place"],
            }
            for earthquake in data["features"]
        ]
        return rows_to_insert
    logger.debug("API Request failed due to %s", response.text)
    raise APIRequestError(f"API request failed with status code {response.status_code}")


def store_in_bigquery(data):
    table = get_settings().bq_table_id
    client = bigquery.Client()
    datastore_event_errors = client.insert_rows_json(
        table, data
    )  # On success returns an empty list
    if not datastore_event_errors:
        logger.info("Data stored successfully.\n---")
    else:
        logger.error("BigQuery datastore encountered errors: %s ", datastore_event_errors)


def validate_latitude(latitude: float) -> None:
    if not (-90.0 <= latitude <= 90.0):
        raise InputValidationError("Latitude must be between -90.0 and 90.0 degrees.")


def validate_longitude(longitude: float) -> None:
    if not (-180.0 <= longitude <= 180.0):
        raise InputValidationError("Longitude must be between -180.0 and 180.0 degrees.")


def validate_radius(radius: float) -> None:
    radius_decimal = Decimal(radius)
    if radius_decimal < Decimal(0) or radius_decimal > Decimal(20001.6):
        raise InputValidationError("Radius must be between 0 and 20001.6 km.")


def validate_time_format(time_str: str) -> datetime:
    try:
        return datetime.fromisoformat(time_str)
    except ValueError as exc:
        raise InputValidationError(f"{time_str} is not a valid ISO8601 format.") from exc


def validate_dates(start_time: str, end_time: str) -> None:
    start_time_dt = validate_time_format(start_time)
    end_time_dt = validate_time_format(end_time)
    if start_time_dt >= end_time_dt:
        raise InputValidationError("Start time must be less than end_time.")
    if end_time_dt > datetime.now():
        raise InputValidationError("End time must be the present time or earlier.")
