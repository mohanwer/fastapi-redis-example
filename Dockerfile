FROM python:3.11 as base


RUN pip install poetry==1.5
WORKDIR app/
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-interaction --no-ansi --no-dev

COPY server server/
FROM base as tests
COPY tests tests/
RUN poetry install --no-interaction --no-ansi
CMD poetry run pytest tests --color=yes

FROM base as production
CMD uvicorn server.main:app --reload
