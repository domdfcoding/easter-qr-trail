#!/usr/bin/env bash
python3 -m gunicorn easter_qr_trail.app:app -w5 --bind 0.0.0.0:8001
