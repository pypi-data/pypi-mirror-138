FROM python:3.7.9-slim

COPY ./docker/local/python/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

WORKDIR /src

COPY ./src/app/requirements /src/app/requirements

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r app/requirements/local_requirements.txt

COPY ./src /src

ENTRYPOINT ["/entrypoint.sh"]