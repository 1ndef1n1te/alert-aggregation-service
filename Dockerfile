FROM python:3.11.9 as build

RUN pip install --no-cache poetry 

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev

FROM python:3.11.9-slim

COPY --from=build .venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY src src

EXPOSE 8000

ENTRYPOINT ["python", "src"]
