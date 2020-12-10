# -*- coding: utf-8 -*-
"""
@time           : 2019/5/24 下午10:22
@author         : liuning11@jd.com
@file           : utils.py
@description    : utils


    ##########################################################
    #
    #
    #
    #
    ##########################################################


"""
import os


def is_exist(file_path):
    return os.path.exists(file_path)


def del_file(file_path):
    os.remove(file_path)


def mkdir(path):
    os.makedirs(path)


def del_dir(dir_path):
    if is_exist(dir_path):
        os.rmdir(dir_path)


def write(path, content):
    with open(path, "w") as fo:
        fo.write(content)


def read(path):
    with open(path, "r") as fo:
        lines = fo.readlines()
    return lines
