# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
@time           : 2019/5/24 下午10:22
@author         : liuning11@jd.com
@file           : gun.py
@description    : gunicorn config


    ##########################################################
    #
    #
    #
    #
    ##########################################################


"""
# Server Socket
bind = '0.0.0.0:8088'
backlog = 2048
# Worker Processes
workers = 20
worker_class = "gevent"
worker_connections = 1000
# Server Mechanics
daemon = False
pidfile = './log/cap-faiss/gunicorn.pid'
# Process Naming
proc_name = 'app_api'
# timeout = 100
# graceful_timeout = 50
# Logging
loglevel = 'error'  # info debug error
accesslog = "./log/cap-faiss/gunicorn-access.log"
errorlog = './log/cap-faiss/gunicorn-error.log'
