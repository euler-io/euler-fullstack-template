#!/bin/bash

set -e

#pip install -r /src/backend/requirements.txt
PYTHONPATH=/src/backend/app python /src/backend/app/start_up.py
PYTHONPATH=/src/backend/app uvicorn main:app --reload --host 0.0.0.0