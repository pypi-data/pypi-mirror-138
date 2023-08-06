import os
from importlib import import_module

settings = import_module(os.environ.get('FASTAPI_SETTINGS', 'app.config.dev_settings'))

def connect(**kwargs):
    raise NotImplementedError()