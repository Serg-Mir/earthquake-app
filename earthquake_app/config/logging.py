from earthquake_app.config.settings import get_settings


def get_logging_config() -> dict:
    return {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {
                "format": "%(levelname)s: [%(name)s:%(funcName)s:%(lineno)s] %(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
        },
        "loggers": {
            "earthquake_app": {
                "handlers": ["console"],
                "propagate": False,
                "level": "DEBUG" if get_settings().debug is True else "INFO",
            },
        },
    }
