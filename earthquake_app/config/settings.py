from functools import lru_cache


from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):
    debug: bool = False
    USGS_API_URL: HttpUrl = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    table_id = "earthquake-data-436210.earthquakes.collected_data"

    # Coordinates of Pleo offices
    office_locations = [
        {"city": "Copenhagen", "lat": 55.6852, "lon": 12.5657},
        {"city": "Paris", "lat": 48.8718, "lon": 2.3259},
        {"city": "Berlin", "lat": 52.5216, "lon": 13.4117},
        {"city": "Lisbon", "lat": 38.7143, "lon": -9.1403},
        {"city": "Madrid", "lat": 40.4345, "lon": -3.7039},
        {"city": "Stockholm", "lat": 59.3360, "lon": 18.0624},
        {"city": "London", "lat": 51.5261, "lon": -0.0744},
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache(maxsize=1)
def get_settings():
    return Settings()
