FROM python:3.13-slim

ARG PORT=8000
ENV PORT=${PORT}

ENV PYTHONPATH=/src \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /src

RUN pip install uv \
    --index-url=https://artifactory.globoi.com/artifactory/api/pypi/pypi/simple

COPY . .

ENV UV_SYSTEM_PYTHON=1

RUN uv pip install --system -e . \
    --index-url=https://artifactory.globoi.com/artifactory/api/pypi/pypi/simple

EXPOSE ${PORT}

ENTRYPOINT []

CMD ["python", "app/main.py"]