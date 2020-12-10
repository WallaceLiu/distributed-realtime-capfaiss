import unittest
import requests
import json
from core_test.base.test_base import http, headers, NpEncoder
import numpy as np


class MetaApiTest(unittest.TestCase):

    def test(self):
        url = '%s/%s' % (http, 'rc/meta')

        data = json.dumps({
            'rcId': 101001101,
            # 'vectors': dsjson.loads(json.dumps(xb, cls=NpEncoder)),
        })

        r = requests.get(url, data=data, headers=headers)
        print("""
        
        url...%s
        head...%s
        content...%s
        
        """ % (url, r.headers, r.content))
