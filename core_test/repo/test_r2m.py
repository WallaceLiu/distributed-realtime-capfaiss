# -*- coding: utf-8 -*-
from core.repo.r2m import R2M
import unittest


class RepoTest(unittest.TestCase):
    def test_r2m_get(self):
        r2m = R2M(**{'host': 'localhost', 'port': 6379})
        v = r2m.get('aaaaa')
        print(v)


if __name__ == '__main__':
    unittest.main()
