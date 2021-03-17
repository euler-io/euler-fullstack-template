#!/bin/bash

pip install -r /src/backend/requirements.txt
PYTHONPATH=/src/backend/app uvicorn main:app --reload --host 0.0.0.0