FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src ./src

RUN pip install --no-cache-dir -e . "fastapi>=0.115" "uvicorn[standard]>=0.30"

EXPOSE 8000

CMD ["uvicorn", "agentbound.server:app", "--host", "0.0.0.0", "--port", "8000"]
