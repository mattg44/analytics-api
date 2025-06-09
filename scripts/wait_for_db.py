import time
import psycopg
import os

RETRIES = 10

while RETRIES > 0:
    try:
        with psycopg.connect(
            dbname=os.environ.get("POSTGRES_DB", "postgres"),
            user=os.environ.get("POSTGRES_USER", "postgres"),
            password=os.environ.get("POSTGRES_PASSWORD", ""),
            host=os.environ.get("POSTGRES_HOST", "db_service"),
            port=int(os.environ.get("POSTGRES_PORT", 5432)),
        ) as conn:
            print("✅ Database is ready!")
            break
    except psycopg.OperationalError as e:
        print("DB not ready yet:", e)
        RETRIES -= 1
        time.sleep(3)

if RETRIES == 0:
    print("Could not connect to the database. Exiting.")
    exit(1)
