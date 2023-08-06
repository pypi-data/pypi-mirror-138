import os
from importlib import import_module
from typing import Any
from datetime import datetime
from urllib import parse

settings = import_module(os.environ.get('FASTAPI_SETTINGS', 'app.config.dev_settings))


def replace_query_param(url: Any, key: Any, val: Any) -> str:
    """
    Given a URL and a key/val pair, set or replace an item in the query
    parameters of the URL, and return the new URL.
    """
    (scheme, netloc, path, query, fragment) = parse.urlsplit(str(url))
    query_dict = parse.parse_qs(query, keep_blank_values=True)
    query_dict[str(key)] = [str(val)]
    query = parse.urlencode(sorted(list(query_dict.items())), doseq=True)
    return parse.urlunsplit((scheme, netloc, path, query, fragment))


def remove_query_param(url: Any, key: Any) -> str:
    """
    Given a URL and a key/val pair, remove an item in the query
    parameters of the URL, and return the new URL.
    """
    (scheme, netloc, path, query, fragment) = parse.urlsplit(str(url))
    query_dict = parse.parse_qs(query, keep_blank_values=True)
    query_dict.pop(key, None)
    query = parse.urlencode(sorted(list(query_dict.items())), doseq=True)
    return parse.urlunsplit((scheme, netloc, path, query, fragment))


def convert_dt_to_string(date_time: datetime) -> str:
    dt_format = getattr(settings, 'DATETIME_FORMAT', '%Y-%m-%d %H:%M:%S')
    return date_time.strftime(dt_format)


def chunk_by_items(items: list, step: int):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(items), step):
        yield items[i : i + step]
