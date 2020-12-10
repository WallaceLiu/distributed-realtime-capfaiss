import unittest
import requests
import json
from core_test.base.test_base import http, headers, NpEncoder
import numpy as np
from core.utils.io_utils import write


class ReindexApiTest(unittest.TestCase):

    def test(self):
        url = '%s/%s' % (http, 'rc/reindex')

        d = 100
        nb = 2000
        np.random.seed(1234)
        xb = np.random.random((nb, d)).astype('float32')
        xb[:, 0] += np.arange(nb) / 1000.

        ids = ['u' + str(i) for i in range(nb)]

        data = json.dumps({
            'rcId': 101001101,
            'ids': ids,
            'vectors': json.loads(json.dumps(xb, cls=NpEncoder)),
        })

        write('./op_reindex_data', json.dumps(data))
        # r = requests.post(url, data=data, headers=headers)
        # print("""
        #
        # url...%s
        # head...%s
        # content...%s
        #
        # """ % (url, r.headers, r.content))
