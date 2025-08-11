import logging.config
import argparse

from earthquake_app.config.logging import get_logging_config
from earthquake_app.process import fetch_earthquakes_near_offices, fetch_earthquakes_custom_zone
from earthquake_app.core import utils


def main():
    logging.config.dictConfig(get_logging_config())

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--lat",
        help="Custom latitude coordinate in degrees. Must be provided together with longitude.",
        type=float,
        required=False,
    )

    parser.add_argument(
        "--lon",
        help="Custom longitude coordinate in degrees. Must be provided together with latitude.",
        type=float,
        required=False,
    )

    parser.add_argument(
        "--start_time",
        help="Start time in ISO8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS). Default is 2023-01-01.",
        type=str,
        required=False,
        default="2023-01-01",
    )

    parser.add_argument(
        "--end_time",
        help="End time in ISO8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS). Default is 2023-12-31.",
        type=str,
        required=False,
        default="2023-12-31",
    )

    parser.add_argument(
        "--radius",
        help="Max radius in kilometers. Must be between 0 and 20001.6 km. Default is 500 km.",
        type=float,
        required=False,
        default=500.0,
    )

    parser.add_argument(
        "--dry_run",
        help="Skip datastore event",
        type=bool,
        required=False,
        default=False,
    )

    # Parse arguments
    args = parser.parse_args()

    # Validate lat and lon conditions
    if args.lat and not args.lon or not args.lat and args.lon:
        parser.error("Either both lat and lon must be set or neither.")
    elif args.lat and args.lon:
        utils.validate_latitude(args.lat)
        utils.validate_longitude(args.lon)
        utils.validate_dates(args.start_time, args.end_time)
        utils.validate_radius(args.radius)

        fetch_earthquakes_custom_zone(
            args.lat, args.lon, args.start_time, args.end_time, args.radius, args.dry_run
        )
    else:
        utils.validate_radius(args.radius)

        fetch_earthquakes_near_offices(args.start_time, args.end_time, args.radius, args.dry_run)


if __name__ == "__main__":
    main()
