# -*- coding: utf-8 -*-
# 开发者:Annona
# 开发时间:2023/11/1 21:10
import redis

if __name__ == '__main__':
    try:
        rs = redis.Redis()
        # 设置redis的值
        # result = rs.set('name', 'annona')
        get_name = rs.get('name')
        print(get_name)
    except Exception as e:
        print(e)

