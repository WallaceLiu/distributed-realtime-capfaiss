import unittest

import redis
from core.model.ufunc import create_item_r2m_key_by_item_and_model_name

r = redis.Redis(host='localhost', port=6379)

user_template_key = 'cupid-sim-{pin}-{model_name}'
item_template_key = 'cupid-sim-{item}-{model_name}'


def pbhmset(l, cnt):
    b = int(len(l) / cnt)
    for i in range(b):
        phmset(l[i * cnt:(i + 1) * cnt])


def phmset(hm):
    with r.pipeline(transaction=False) as p:
        for d in hm:
            p.hmset(d[0], d[1])
        result = p.execute()
    return result


def test_r2m_item_id_mapper(template_key, model_name_no_dt, dt):
    data_hash = []

    items_id_mapper = []
    for i in range(8000):
        items_id_mapper.append((i, 'jd_%s' % (i * 1000)))

    for item in items_id_mapper:
        key = \
            create_item_r2m_key_by_item_and_model_name(template_key,
                                                       item[0],
                                                       model_name_no_dt)
        data_hash.append((key, {'item_id': item[1], 'dt': dt}))

    for d in data_hash[:10]:
        print(d)

    pbhmset(data_hash, 1000)
    print('end.')


#
test_r2m_item_id_mapper(item_template_key,
                        'sim_dmcqm_lhmx_sku_rec_faiss_item_vec_scene102002_v1_s_d_d100_e100', '2020-03-18')
