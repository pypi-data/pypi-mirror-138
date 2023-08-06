import os
import json_log_formatter
import logging
from datetime import datetime
from importlib import import_module
from pydantic import BaseModel

settings = import_module(os.environ.get('FASTAPI_SETTINGS', 'app.config.dev_settings'))  # type: ignore


class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        extra['level'] = record.levelname
        extra['time'] = datetime.now().isoformat()
        extra['module'] = str(record.module)
        extra['name'] = record.name
        extra['filename'] = record.filename
        extra['path_name'] = record.pathname
        extra['proccess_name'] = record.processName
        extra['message'] = message
        extra['project_name'] = settings.PROJECT_NAME

        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)
            extra['exception'] = True
        else:
            extra['exception'] = False
            extra['exc_info'] = None

        return extra


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "app"
    LOG_FORMAT: str = '{"level": "%(levelname)s", "module": "%(module)s", "asctime", "%(asctime)s", "log_message": "%(message)s"}'
    LOG_LEVEL: str = os.environ.get("FASTAPI_LOG_LEVEL", "DEBUG")

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {'json': {'()': 'app.config.log.CustomisedJSONFormatter'}}
    handlers = {
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'filename': os.path.join(settings.BASE_DIR, 'data.log'),  # type: ignore
            'formatter': 'json',
        },
    }

    loggers = {'app': {'handlers': ['file'], 'level': LOG_LEVEL, 'propagate': True,}}
