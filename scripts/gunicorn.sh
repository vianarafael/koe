#!/bin/bash

# Run production server with gunicorn

source .venv/bin/activate
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:8000
