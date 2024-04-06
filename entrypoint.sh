#!/bin/bash

# Set up signal handling
python uvicorn_config.py

# Start uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 80
