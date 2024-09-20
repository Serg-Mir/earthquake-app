from google.cloud import bigquery
from earthquake_app.config.settings import get_settings
from earthquake_app.core.clients import USGSClient
import logging


logger = logging.getLogger("earthquake_app.utils")


def fetch_earthquake_data(lat, lon, start_time, end_time, radius):
    client = USGSClient()
    params = {
        "format": "geojson",
        "starttime": start_time,
        "endtime": end_time,
        "latitude": lat,
        "longitude": lon,
        "maxradiuskm": radius
    }
    response = client.request("GET", params=params)
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
    raise Exception(f"API request failed with status code {response.status_code}")


def store_in_bigquery(data, table=get_settings().table_id):
    client = bigquery.Client()
    datastore_event = client.insert_rows_json(table, data)
    if not datastore_event:
        logger.info("Data stored successfully.\n---")
    else:
        logger.error(f"BigQuery datastore encountered errors: {datastore_event}")


def validate_dates(start_time, end_time):
    if start_time >= end_time:
        raise ValueError("Start time must be before end time for %s, %s" % (start_time, end_time))
