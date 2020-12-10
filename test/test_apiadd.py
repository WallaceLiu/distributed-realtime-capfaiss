import unittest
import requests
import json
from core_test.base.test_base import http, headers, NpEncoder
import numpy as np
from core.utils.io_utils import write


class AddApiTest(unittest.TestCase):

    def test(self):
        url = '%s/%s' % (http, 'rc/add')
        print(url)

        d = 100
        nb = 2000
        np.random.seed(4567)
        xb = np.random.random((nb, d)).astype('float32')
        xb[:, 0] += np.arange(nb) / 2000.

        ids = ['u' + str(i + nb) for i in range(1, nb + 1)]

        data = json.dumps({
            'rcId': 101001101,
            'ids': ids,
            'vectors': json.loads(json.dumps(xb, cls=NpEncoder)),
        })

        write('./op_add_data', json.dumps(data))

        # r = requests.post(url, data=data, headers=headers)
        # print("""
        #
        # url...%s
        # content...%s
        #
        # """ % (url, r.content))
