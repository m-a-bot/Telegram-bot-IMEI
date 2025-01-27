FROM python:3.12-alpine3.20

ENV PYTHONPATH=/src

ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /src

COPY ./app /src/app
COPY ["./pyproject.toml", ".env", "/src/"]

EXPOSE 8443

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

CMD ["poetry", "run", "python", "app/bot.py"]