FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

COPY models/ ./models/
COPY src/ ./src/

EXPOSE 8000

CMD ["uvicorn", "src.main:api", "--host", "0.0.0.0", "--port", "8000"]
