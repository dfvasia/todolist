FROM python:3.10-slim

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - && poetry --version

WORKDIR project/
COPY poetry.lock
COPY po