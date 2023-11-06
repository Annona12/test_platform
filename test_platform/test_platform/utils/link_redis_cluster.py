# -*- coding: utf-8 -*-
# 开发者:Annona
# 开发时间:2023/11/4 13:26
from rediscluster import *

if __name__ == '__main__':
    try:
        # 构建所有的节点，Redis会使⽤CRC16算法，将键和值写到某个节点上
        startup_nodes = [
            {'host':'127.0.0.1','port':'6379'},
            {'host': '127.0.0.1', 'port': '6380'},
            {'host': '127.0.0.1', 'port': '6381'}
        ]
        # 构建StrictRedisCluster对象
        src = RedisCluster(startup_nodes=startup_nodes)
        result = src.set('test1','test')
        print(result)
    except Exception as e:
        print(e)