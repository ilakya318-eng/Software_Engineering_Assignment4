FROM python:3.12-slim

WORKDIR /app

COPY campus_model.py .
COPY test_campus.py .

RUN pip install --no-cache-dir pytest

CMD ["python", "-m", "pytest", "-v"]
