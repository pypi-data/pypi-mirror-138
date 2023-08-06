version: '3.7'
services:
  python: &python
    networks:
      - {{ params['network'] }}
    image: {{ params['registry'] }}/{{ params['project_name'] }}/{{ params['project_name'] }}
    build:
      context: .
      dockerfile: docker/prod/python/Dockerfile
    environment:
      DJANGO_SETTINGS_MODULE: "{{ params['project_name'] }}.settings.prod"
      AWS_PROFILE: "default"
    volumes:
     - ~/.aws/:/root/.aws
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
          memory: 64M
    command: gunicorn {{ params['project_name'] }}.wsgi -b 0.0.0.0:8000
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
        delay: 10s
        max_attempts: 4
        window: 120s
      resources:
        limits:
          memory: 768M
        reservations:
          memory: 32M
    command: celery -A {{params['project_name'] }} worker -Q {{ params['project_name'] }}_default -c 2 --loglevel=info --max-tasks-per-child=1
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
        delay: 10s
        max_attempts: 4
        window: 120s
      resources:
        limits:
          cpus: "0.15"
          memory: 64M
        reservations:
          cpus: "0.05"
          memory: 32M
    command: celery -A {{params['project_name'] }} beat --loglevel=info
    ports: []
    depends_on:
      - celery_worker_default

networks:
  {{ params['network'] }}:
    external: true