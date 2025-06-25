import os, psycopg2
from psycopg2.extras import execute_values

SEED = int(os.getenv("SEED_COUNT", "50"))

conn = psycopg2.connect(
    host="haproxy",
    port=5001,
    user=os.getenv("FLYWAY_USER", "myuser"),
    password=os.getenv("FLYWAY_PASSWORD", "mypassword"),
    dbname="postgres",
)
conn.autocommit = True
cur = conn.cursor()

def table_exists(name: str) -> bool:
    cur.execute(
        "SELECT 1 FROM information_schema.tables "
        "WHERE table_schema='public' AND table_name=%s", (name.lower(),)
    )
    return cur.fetchone() is not None

def insert_returning(sql: str, rows, id_column: str, table: str):
    result = execute_values(cur, sql, rows, fetch=True)
    ids = [r[0] for r in (result or [])]
    if not ids:
        cur.execute(f"SELECT {id_column} FROM {table}")
        ids = [r[0] for r in cur.fetchall()]
    return ids