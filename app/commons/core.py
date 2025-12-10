"""Core module."""

import os
import json

import logging
import functools
from datetime import datetime


log_level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
numeric_log_level = getattr(logging, log_level_name, logging.INFO)

logging.basicConfig(
    level=numeric_log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True,
)
logger = logging.getLogger(__name__)

logging.getLogger().setLevel(numeric_log_level)
logger.setLevel(numeric_log_level)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):  # type: ignore
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


original_dumps = json.dumps
json.dumps = functools.partial(original_dumps, cls=DateTimeEncoder)

logging.info("Applied custom JSON encoder for datetime serialization")
