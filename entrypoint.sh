#!/bin/bash
case "$1" in
  watch)
    echo "Launching Watcher..."
    python app/watch_desktop.py
    ;;
  ingest)
    echo "Launching Ingest Worker..."
    python app/ingest_files.py
    ;;
  api)
    echo "Launching API..."
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ;;
  *)
    echo "Usage: watch | ingest | api"
    exit 1
    ;;
esac
