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
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'User-Agent': 'Mozilla/5.0',
    'content-type': 'application/json',
    'charset': 'UTF-8',
}


# @elapsed_time
def AddApiTest(host, port, rc_id, num):
    url = 'http://{host}:{port}/{url}'.format(host=host, port=port, url='rc/add')
    print(url)

    d = 100
    nb = num
    np.random.seed(4567)
    xb = np.random.random((nb, d)).astype('float32')
    xb[:, 0] += np.arange(nb) / 2000.

    ids = ['u' + str(i + nb) for i in range(1, nb + 1)]

    data = json.dumps({
        'rcId': rc_id,
        'ids': ids,
        'vectors': json.loads(json.dumps(xb, cls=NpEncoder)),
    })

    s = requests.session()
    req = s.post(url, data=data, headers=headers)
    return req


if __name__ == '__main__':
    print('test begin...')

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost', required=False, help='')
    parser.add_argument('--port', type=str, default='8088', required=False, help='')
    parser.add_argument('--rc_id', type=str, default='101001101', required=False, help='')
    parser.add_argument('--num', type=int, default=10000, required=False, help='')

    params = parser.parse_args()

    req = AddApiTest(params.host, params.port, params.rc_id, params.num)

    print("""
            add
            status_code...%s
            content...%s

            """ % (req.status_code, req.content))
