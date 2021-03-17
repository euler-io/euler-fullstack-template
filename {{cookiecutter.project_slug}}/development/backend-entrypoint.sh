#!/bin/bash

PYTHONPATH=/src/backend/app uvicorn main:app --reload --host 0.0.0.0