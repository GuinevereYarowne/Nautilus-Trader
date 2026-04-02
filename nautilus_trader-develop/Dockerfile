FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -e .[dev]
CMD ["python", "test_custom_aggregator.py"]