
FROM ghcr.io/astral-sh/uv:0.13.5 AS uv

FROM python:3.13-slim

WORKDIR /app

COPY --from=uv /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY src/ ./src/
COPY model/ ./model/

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
