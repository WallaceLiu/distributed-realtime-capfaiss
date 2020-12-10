#!/bin/bash
#
# Usage: start.sh
#
nohup gunicorn -c gun.py ../app_api_alone:app >>/export/servers/log/cap-faiss/detail.log 2>&1 &
