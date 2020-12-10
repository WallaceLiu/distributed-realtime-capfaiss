import unittest
import requests
import json
from core_test.base.test_base import http, headers, NpEncoder
import numpy as np
from core.utils.io_utils import write


class SearchApiTest(unittest.TestCase):

    def test(self):
        url = '%s/%s' % (http, 'rc/search')

        d = 100
        nb = 2000
        np.random.seed(1234)
        xb = np.random.random((nb, d)).astype('float32')
        xb[:, 0] += np.arange(nb) / 1000.

        ids = ['u' + str(i) for i in range(1)]

        data = json.dumps({
            'rcId': "101001101",
            'ids': ids,
            'vectors': json.loads(json.dumps(xb[0:1], cls=NpEncoder)),
        })

        write('./op_searc_data', json.dumps(data))

        # r = requests.post(url, data=data, headers=headers)
        # print("""
        #
        # url...%s
        # content...%s
        #
        # """ % (url, r.content))
