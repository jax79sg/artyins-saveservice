#!/bin/bash
source venv/bin/activate
gunicorn --daemon  --bind 0.0.0.0:9898 --workers 1 wsgi:app
