import time, random, prometheus_client, psycopg2, os
from sql_queries import STATEMENTS
REQUEST_LAT = prometheus_client.Summary('sql_request_seconds','latency',['query'])
prometheus_client.start_http_server(8000)

conn = psycopg2.connect(
    host=os.getenv("PGHOST", "haproxy"),
    port=os.getenv("PGPORT", "5001"),
    dbname=os.getenv("PGDATABASE", "postgres"),
    user=os.getenv("PGUSER", "myuser"),
    password=os.getenv("PGPASSWORD", "mypassword"),
)
print("Начало loadtest")
start_time = time.time()
while True:
    elapsed_time = time.time() - start_time
    print(f"Прошло времени с начала работы: {elapsed_time:.2f} секунд")
    cur = conn.cursor()
    for name, sql in STATEMENTS.items():
        start = time.perf_counter()
        print(sql)
        cur.execute(sql); cur.fetchall()
        REQUEST_LAT.labels(name).observe(time.perf_counter()-start)
    time.sleep(random.uniform(0.2, 1))