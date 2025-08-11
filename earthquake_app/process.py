import logging.config
from earthquake_app.core.utils import fetch_earthquake_data, store_in_bigquery
from earthquake_app.config.settings import get_settings

from pydantic import BaseModel, Field


class EarthquakeQuery(BaseModel):
    lat: float
    lon: float
    start_date: str
    end_date: str
    radius: float
    dry_run: bool = Field(default=False)


logger = logging.getLogger(__name__)


def fetch_earthquakes_near_offices(
    start_date: str, end_date: str, radius: float, dry_run: bool = False
):
    for office in get_settings().locations:
        data = fetch_earthquake_data(office["lat"], office["lon"], start_date, end_date, radius)
        if data:
            logger.info("Earthquake data found for %s", data[0]["place"])
            if not dry_run:
                store_in_bigquery(data)
        else:
            logger.info("Earthquake data not found for %s", office["city"])


def fetch_earthquakes_custom_zone(query: EarthquakeQuery):
    data = fetch_earthquake_data(
        query.lat, query.lon, query.start_date, query.end_date, query.radius
    )
    if data:
        logger.info("Earthquake data found for %s", data[0]["place"])
        if not query.dry_run:
            store_in_bigquery(data)
    else:
        logger.info("No relevant data found")
