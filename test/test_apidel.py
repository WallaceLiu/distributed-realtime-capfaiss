import unittest
import requests
import json
from core_test.base.test_base import http, headers, NpEncoder
import numpy as np
from core.utils.io_utils import write


class DelApiTest(unittest.TestCase):

    def test(self):
        url = '%s/%s' % (http, 'rc/del')

        ids = ['u' + str(i) for i in range(10)]

        data = json.dumps({
            'rcId': 101001101,
            'ids': ids,
        })

        # write('./op_del_data', json.dumps(data))

        r = requests.post(url, data=data, headers=headers)
        print("""

        url...%s
        content...%s

        """ % (url, r.content))
