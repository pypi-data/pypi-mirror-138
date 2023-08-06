import os.path
from typing import Any, MutableMapping

import structlog

from starlette_context import context

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
    },
    "handlers": {
        "json": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
        "request_log": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "./logs/request_log.log",
            "formatter": "json",
        },
        "all": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./logs/all.log",
            "maxBytes": 10485760,  # 10MB #1024*1024*10
            "backupCount": 50,
            "encoding": "utf8",
            "formatter": "json",
        },
    },
    "loggers": {
        "request": {
            "handlers": ["json", "all", "request_log"],
            "level": "INFO",
        },
        # "uvicorn": {"handlers": ["json"], "level": "INFO"},
        # "uvicorn.error": {"handlers": ["json"], "level": "INFO"},
        # "uvicorn.access": {
        #     "handlers": ["json"],
        #     "level": "INFO",
        #     "propagate": False,
        # },
    },
}


def setup_logging():
    import logging.config

    def add_app_context(
            logger: logging.Logger,
            method_name: str,
            event_dict: MutableMapping[str, Any],
    ) -> MutableMapping[str, Any]:
        if context.exists():
            event_dict.update(context.data)
        return event_dict

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            add_app_context,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.AsyncBoundLogger,
        cache_logger_on_first_use=True,
    )

    log_path = "./logs"
    if not os.path.exists(path=log_path):
        os.makedirs(log_path)

    logging.config.dictConfig(logging_config)
