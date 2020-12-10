import sys

sys.path.append('core.zip')
import json
import numpy as np
from core.utils.utils import NpEncoder
import requests
import argparse
from core.utils.udecorator import elapsed_time
import time

headers = {
    'User-Agent': 'Mozilla/5.0',
    'content-type': 'application/json',
    'charset': 'UTF-8',
}


# @elapsed_time
def ReindexApiTest(host, port, rc_id, num):
    url = 'http://{host}:{port}/{url}'.format(host=host, port=port, url='rc/reindex')
    d = 100
    nb = num
    np.random.seed(1234)
    xb = np.random.random((nb, d)).astype('float32')
    xb[:, 0] += np.arange(nb) / 1000.

    ids = ['u' + str(i) for i in range(nb)]

    data = json.dumps({
        'rcId': rc_id,
        'ids': ids,
        'vectors': json.loads(json.dumps(xb, cls=NpEncoder)),
    })

    s = requests.session()
    r = s.post(url, data=data, headers=headers)
    return r


if __name__ == '__main__':
    print('test begin...')

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost', required=False, help='')
    parser.add_argument('--port', type=str, default='8088', required=False, help='')
    parser.add_argument('--rc_id', type=str, default='101001101', required=False, help='')
    parser.add_argument('--num', type=int, default=1000, required=False, help='')

    params = parser.parse_args()

    req = ReindexApiTest(params.host, params.port, params.rc_id, params.num)

    print("""
            reindex
            status_code...%s
            content...%s

            """ % (req.status_code, req.content))
