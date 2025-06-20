FROM python:3.13 as builder

RUN pip3 install poetry==2.1.3
WORKDIR /app
COPY pyproject.toml poetry.lock README.md /app/

ENV POETRY_NO_INTERACTION=1 \
POETRY_VIRTUALENVS_IN_PROJECT=1 \
POETRY_VIRTUALENVS_CREATE=true \
POETRY_CACHE_DIR=/tmp/poetry_cache

RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --no-root

FROM python:3.13 as runner
WORKDIR /app
COPY src /app/src/

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
