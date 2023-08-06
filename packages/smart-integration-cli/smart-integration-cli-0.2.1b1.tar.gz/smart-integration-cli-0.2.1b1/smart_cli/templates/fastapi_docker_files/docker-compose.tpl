version: "3.7"
services:
  {{ params['project_name'] }}_python: &{{ params['project_name'] }}_python # link to instance
    build:
      context: .
      dockerfile: docker/local/python/Dockerfile
    volumes:
      - ./src:/src
      - ~/.aws/:/home/user/.aws:ro
    ports:
      - 8000:8000
    environment:
      AWS_PROFILE: "default"
      FASTAPI_SETTINGS: "app.config.dev_settings"
      FASTAPI_APP_TYPE: "dev"
      FASTAPI_LOG_LEVEL: "DEBUG"
    command: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    depends_on:
      - {{ params['project_name'] }}_rabbitmq
      - {{ params['project_name'] }}_celery_worker_default
  {{ params['project_name'] }}_rabbitmq:
    image: rabbitmq:3.7-alpine
  {{ params['project_name'] }}_celery_worker_default:
    <<: *{{ params['project_name'] }}_python # up to copy of instance
    command: celery worker -A app.core.celery --loglevel info
    ports: []
    depends_on:
      - {{ params['project_name'] }}_rabbitmq
  {{ params['project_name'] }}_celery_beat:
    <<: *{{ params['project_name'] }}_python # up to copy of instance
    command: celery -A app.core.celery beat --loglevel=info
    ports: []
    depends_on:
      - {{ params['project_name'] }}_rabbitmq
      - {{ params['project_name'] }}_celery_worker_default
