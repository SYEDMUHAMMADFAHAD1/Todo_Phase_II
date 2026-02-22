#!/bin/bash
# Railway entrypoint script
# PORT environment variable is set by Railway automatically

echo "Starting server on port ${PORT:-8000}..."
exec python run_server.py
