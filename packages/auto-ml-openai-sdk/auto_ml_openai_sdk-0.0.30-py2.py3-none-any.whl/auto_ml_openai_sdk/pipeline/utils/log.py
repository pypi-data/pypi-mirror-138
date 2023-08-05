import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s.%(msecs)03d %(levelname)s:[%(name)s] %(message)s",
            "datefmt": "%m/%d/%Y %H:%M:%S",
        }
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "pipeline": {"handlers": ["default"], "level": "INFO", "propagate": False}
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
