# -*- coding: utf-8 -*-
from core.utils.udecorator import *


@singleton
class Foo:
    def __new__(cls):
        cls.x = 10
        return object.__new__(cls)

    def __init__(self):
        assert self.x == 10
        self.x = 15


assert Foo().x == 15
Foo().x = 20
assert Foo().x == 20
