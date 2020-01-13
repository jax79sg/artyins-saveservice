#!/bin/bash
source venv/bin/activate
gunicorn --daemon  --bind 0.0.0.0:9891 --workers 1 wsgi:app
