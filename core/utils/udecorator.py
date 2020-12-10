# -*- coding: utf-8 -*-
"""
@time           : 2019/5/24 下午10:22
@author         : liuning11@jd.com
@file           : udecorator.py
@description    : udecorator


    ##########################################################
    #
    #
    #
    #
    ##########################################################


"""
import datetime
import functools
import time
import logging
from queue import Queue
from threading import Thread
import threading


def elapsed_time(func):
    """
    elapsed time of function
    :param func:
    :return:
    """

    def wrapper(*args, **kw):
        start_time = datetime.datetime.now()
        res = func(*args, **kw)
        over_time = datetime.datetime.now()
        etime = (over_time - start_time).total_seconds()
        logging.info('Elapsed time: current function <{0}> is {1} s'.format(func.__name__, etime))
        return res

    return wrapper


class asynchronous(object):
    """
    asynchronous
    """

    def __init__(self, func):
        self.func = func

        def threaded(*args, **kwargs):
            self.queue.put(self.func(*args, **kwargs))

        self.threaded = threaded

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def start(self, *args, **kwargs):
        self.queue = Queue()
        thread = Thread(target=self.threaded, args=args, kwargs=kwargs);
        thread.start();
        return asynchronous.Result(self.queue, thread)

    class NotYetDoneException(Exception):
        def __init__(self, message):
            self.message = message

    class Result(object):
        def __init__(self, queue, thread):
            self.queue = queue
            self.thread = thread

        def is_done(self):
            return not self.thread.is_alive()

        def get_result(self):
            if not self.is_done():
                raise asynchronous.NotYetDoneException('the call has not yet completed its task')

            if not hasattr(self, 'result'):
                self.result = self.queue.get()

            return self.result


def singleton(cls):
    """
    Use class as singleton.
    :param cls:
    :return:
    """

    cls.__new_original__ = cls.__new__

    @functools.wraps(cls.__new__)
    def singleton_new(cls, *args, **kw):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it

        cls.__it__ = it = cls.__new_original__(cls, *args, **kw)
        it.__init_original__(*args, **kw)
        return it

    cls.__new__ = singleton_new
    cls.__init_original__ = cls.__init__
    cls.__init__ = object.__init__

    return cls


def synchronized(func):
    """
    simple lock
    :param func:
    :return:
    """
    func.__lock__ = threading.Lock()

    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func

#
# def modelsingleton(cls):
#     """
#     Use model as singleton.
#     :param cls:
#     :return:
#     """
#
#     cls.__new_original__ = cls.__new__
#
#     @functools.wraps(cls.__new__)
#     def singleton_new(cls, *args, **kw):
#         _dt = YESTERDAY if 'dt' not in kw else kw['dt']
#         _code = '%s%s%s' % (json.dumps(args).replace(' ', ''), json.dumps(kw).replace(' ', ''), _dt)
#         code = hashlib.md5(_code.encode(encoding='UTF-8')).hexdigest()
#         it = cls.__dict__.get('__it__')
#         if it is not None and cls.code == code:
#             return it
#
#         cls.__it__ = it = cls.__new_original__(cls, *args, **kw)
#         it.__init_original__(*args, **kw)
#         return it
#
#     cls.__new__ = singleton_new
#     cls.__init_original__ = cls.__init__
#     cls.__init__ = object.__init__
#
#     return cls
