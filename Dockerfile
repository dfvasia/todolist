FROM python:3.10-slim

RUN apt-get update && apt-get upgrade -y && apt-get install -y curl libpq-dev python3-dev build-essential dos2unix
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="/root/.poetry/bin:$PATH"

WORKDIR project/
COPY poetry.lock pyproject.toml /project/

RUN poetry config virtualenvs.create false --local
RUN poetry install

COPY . .
RUN ["chmod", "+x", "./start_p.sh"]
RUN dos2unix ./start_p.sh