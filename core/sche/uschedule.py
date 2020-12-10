# -*- coding: utf-8 -*-
"""
@time           : 2019/5/24 下午10:22
@author         : liuning11@jd.com
@file           : uschedule.py
@description    : schedules


    ##########################################################
    #
    #
    #
    #
    ##########################################################


"""
import time
from apscheduler.schedulers.background import BackgroundScheduler


def elect_master(ha):
    ha.create_instance()
    ha.choose_master()
    while 1:
        time.sleep(10)


def scheduler_start(context):  # cache_r2m, cache_local, APP_UUID
    sche = BackgroundScheduler()
    sche.add_job(elect_master, "interval", seconds=20, args=[context.contain['ha']], id='elect_master')
    # sche.add_job(index_persit, "interval", seconds=20,
    #              args=[context.contain['ha'], context.contain['index_persit'], context.contain['index_man']],
    #              id='index_persit')
    # sche.add_job(index_persit, "interval", minutes=20,
    #              args=[model_man, 'sim', [102002, 106020, 106033], context, cache_r2m, cache_local, APP_UUID],
    #              id='monitor_pid_sim_item_id_mapper')
    sche.start()
    return sche
