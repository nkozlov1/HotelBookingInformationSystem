FROM python:3.12-slim
WORKDIR /app
RUN pip install psycopg2-binary prometheus_client
COPY stress.py .
COPY sql_queries.py .
CMD ["python", "stress.py"]