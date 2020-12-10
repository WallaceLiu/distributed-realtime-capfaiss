import redis
from redis import WatchError
from concurrent.futures import ProcessPoolExecutor

r = redis.Redis(host='127.0.0.1', port=6379)


# 减库存函数, 循环直到减库存完成
# 库存充足, 减库存成功, 返回True
# 库存不足, 减库存失败, 返回False
def decr_stock():
    # python中redis事务是通过pipeline的封装实现的
    with r.pipeline() as pipe:
        while True:
            try:
                # watch库存键, multi后如果该key被其他客户端改变, 事务操作会抛出WatchError异常
                pipe.watch('stock:count')
                count = int(pipe.get('stock:count'))
                if count > 0:  # 有库存
                    # 事务开始
                    pipe.multi()
                    pipe.decr('stock:count')
                    # 把命令推送过去
                    # execute返回命令执行结果列表, 这里只有一个decr返回当前值
                    print
                    pipe.execute()[0]
                    return True
                else:
                    return False
            except WatchError as  ex:
                # 打印WatchError异常, 观察被watch锁住的情况
                print(ex)
                pipe.unwatch()


def worker():
    while True:
        # 没有库存就退出
        if not decr_stock():
            break


# 实验开始
# 设置库存为100
r.set("stock:count", 100)

# 多进程模拟多个客户端提交
with ProcessPoolExecutor(max_workers=2) as pool:
    for _ in range(10):
        pool.submit(worker)
