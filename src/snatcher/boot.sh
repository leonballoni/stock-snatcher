#!/bin/bash
poetry env use python && \
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --workers 3 --log-level info
