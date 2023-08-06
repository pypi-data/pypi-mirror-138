import os

PROJECT_NAME = "{{ params['project_name'] }}"
PROJECT_DESCRIPTION = (
    "{{ params['project_name'] }} Application"
)
SERVER_HOST = 'http://127.0.0.1:8000'

# Secret key
SECRET_KEY = '{{ params['secret_key'] }}'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FASTAPI_APP_PATH = os.environ.get('FASTAPI_APP_PATH', '{{ params['project_name'] }}')
API_PATH = f"{FASTAPI_APP_PATH}/api"

ACCESS_TOKEN_EXPIRE_SECONDS = 3600 * 24 * 30
REFRESH_TOKEN_EXPIRE_SECONDS = 3600 * 24 * 365

# CORS
BACKEND_CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:4200",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:8081",
]

DT_FORMAT = '%Y-%m-%d %H:%M:%S'

from celery.schedules import crontab

CELERY_BROKER_URL = 'amqp://{{ params['project_name'] }}_rabbitmq'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

CREDENTIAL_MODEL = 'app.credentials.models.Credential'