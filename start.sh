#!/bin/sh
echo "🔄 Waiting for database to be ready..."
python scripts/wait_for_db.py

echo "🚀 Starting FastAPI app..."
exec .venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 80 --reload
