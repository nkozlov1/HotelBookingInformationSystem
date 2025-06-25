FROM python:3.12-slim-bullseye

RUN apt-get update \
 && apt-get install -y --no-install-recommends postgresql-client

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x run_seeder.sh

CMD ["./run_seeder.sh"]