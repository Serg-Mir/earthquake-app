import logging.config
from earthquake_app.core.utils import fetch_earthquake_data, store_in_bigquery
from earthquake_app.config.settings import get_settings

logger = logging.getLogger(__name__)


def fetch_earthquakes_near_offices(start_date: str, end_date: str, radius: float):
    for office in get_settings().office_locations:
        data = fetch_earthquake_data(office["lat"], office["lon"], start_date, end_date, radius)
        if data:
            logger.info("Earthquake data found for %s", data[0]["place"])
            store_in_bigquery(data)
        else:
            logger.info("Earthquake data not found for %s", office["city"])


def fetch_earthquakes_custom_zone(
    lat: float, lon: float, start_date: str, end_date: str, radius: float
):
    data = fetch_earthquake_data(lat, lon, start_date, end_date, radius)
    if data:
        logger.info("Earthquake data found for %s", data[0]["place"])
        store_in_bigquery(data)
    else:
        logger.info("No relevant data found")
