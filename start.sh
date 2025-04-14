#!/bin/bash
/opt/render/project/.venv/bin/python -m gunicorn canteen_backend.wsgi:application --bind 0.0.0.0:$PORT