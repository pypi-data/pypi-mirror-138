version: "3.7"
services:
  python: &python # link to instance
    image: {{ params['registry'] }}/{{ params['project_name'] }}/{{ params['project_name'] }}
    networks:
      - {{ params['network'] }}
    build:
      context: .
      dockerfile: docker/prod/python/Dockerfile
    volumes:
      - ~/.aws/:/root/.aws:ro
    environment:
      AWS_PROFILE: "default"
      FASTAPI_SETTINGS: "app.config.prod_settings"
      FASTAPI_APP_TYPE: "prod"
      FASTAPI_APP_PATH: "/{{ params['project_name'] }}"
      FASTAPI_LOG_LEVEL: "INFO"
    deploy:
      update_config:
        order: start-first
        failure_action: rollback
        monitor: 3s
        delay: 5s
      rollback_config:
        parallelism: 0
        order: stop-first
      restart_policy:
        condition: on-failure
        delay: 10s
        max_attempts: 4
        window: 120s
      resources:
        limits:
          cpus: "0.25"
          memory: 256M
        reservations:
          cpus: "0.05"
          memory: 128M
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
  celery_worker_default:
    <<: *python # up to copy of instance
    deploy:
      update_config:
        order: start-first
        failure_action: rollback
        monitor: 3s
        delay: 5s
      rollback_config:
        parallelism: 0
        order: stop-first
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 2
        window: 60s
      resources:
        limits:
          cpus: "0.25"
          memory: 756M
        reservations:
          cpus: "0.05"
          memory: 128M
    command: celery worker -A app.core.celery --loglevel info -c 3 --max-tasks-per-child 1
    ports: []
  celery_beat:
    <<: *python # up to copy of instance
    deploy:
      update_config:
        order: start-first
        failure_action: rollback
        monitor: 3s
        delay: 5s
      rollback_config:
        parallelism: 0
        order: stop-first
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 2
        window: 60s
      resources:
        limits:
          cpus: "0.15"
          memory: 128M
        reservations:
          cpus: "0.02"
          memory: 26M
    command: celery -A app.core.celery beat --loglevel=info
    ports: []
    depends_on:
      - celery_worker_default


networks:
  {{ params['network'] }}:
    external: true