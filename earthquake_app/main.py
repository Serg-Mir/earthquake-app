import logging.config
from earthquake_app.config.logging import get_logging_config
import argparse
from earthquake_app.process import fetch_earthquakes_near_offices, fetch_earthquakes_custom_zone
from earthquake_app.core.utils import validate_dates


def main():
    # Configuring Python logging.
    logging.config.dictConfig(get_logging_config())

    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", help="Custom coordinates for LAT", type=float, required=False)
    parser.add_argument("--lon", help="Custom coordinates for LON", type=float, required=False)
    parser.add_argument("--start_time", help="Format: YYYY-MM-DD", type=str, required=False,
                        default="2023-01-01")
    parser.add_argument("--end_time", help="Format: YYYY-MM-DD", type=str, required=False,
                        default="2023-12-31")
    parser.add_argument("--radius", help="Max radius in KM", type=int, required=False,
                        default=500)

    # Parse arguments
    args = parser.parse_args()

    validate_dates(args.start_time, args.end_time)

    # Validate lat and lon existence
    if args.lat and not args.lon or not args.lat and args.lon:
        parser.error("Either both lat and lon must be set or neither.")
    elif args.lat and args.lon:
        fetch_earthquakes_custom_zone(args.lat, args.lon, args.start_time, args.end_time, args.radius)
    else:
        fetch_earthquakes_near_offices(args.start_time, args.end_time, args.radius)


if __name__ == "__main__":
    main()
