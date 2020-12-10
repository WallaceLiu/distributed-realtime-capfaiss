#!/bin/bash
#
# Usage: start.sh
#
chmod u+x *.sh
nohup gunicorn -c gun.py ../app_api_cluster:app >>./log/cap-faiss/detail.log 2>&1 &
nohup python ../app_rpc.py >>./log/cap-faiss/detail-rpc.log 2>&1 &
python ../app_rpc_master.py
