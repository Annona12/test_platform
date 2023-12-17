# -*- coding: utf-8 -*-
# 开发者:Annona
# 开发时间:2023/12/17 13:11

# 如果用户通过QQ或者账号登录了，则将cookies中的购物车数据合并到redis中
import base64
import pickle

from django_redis import get_redis_connection


def merge_carts_cookies_redis(request, user, response):
    """
    :param request:
    :param user:
    :param response:
    :return:
    """
    # 1、在QQ登录或者账号登录的时候，将cookies中的数据合并到redis中
    # 2、获取cookies中的购物车数据
    cart_str = request.COOKIES.get('carts')
    # 如果cookies中不存在购物车数据，则直接返回redis中的数据
    if not cart_str:
        return response
    # 将 cart_str转成bytes类型的字符串
    cookie_cart_str_bytes = cart_str.encode()
    # 将cart_str_bytes转成bytes类型的字典
    cookie_cart_dict_bytes = base64.b64decode(cookie_cart_str_bytes)
    # 将cookie_cart_dict_bytes转换成真正的字典
    cookie_cart_dict = pickle.loads(cookie_cart_dict_bytes)

    # 准备新的数据容器：保存新的sku_id、count、selected，unsele
    new_cart_dict = {}
    new_selected_add = []
    new_selected_rem = []
    # 遍历cookies中的数据
    for sku_id ,cookie_dict in cookie_cart_dict.items():
        new_cart_dict[sku_id] = cookie_dict['count']
        if cookie_dict['selected']:
            new_selected_add.append(sku_id)
        else:
            new_selected_rem.append(sku_id)
    # 3、将cookies中的购物车数据合并到redis中
    redis_conn = get_redis_connection('carts')
    pl = redis_conn.pipeline()
    pl.hmset('carts_%s' % user.id,new_cart_dict)
    if new_selected_add:
        pl.sadd('selected_%s' % user.id,*new_selected_add)
    else:
        pl.srem('selected_%s' % user.id, *new_selected_rem)
    pl.execute()

    # 删除cookies
    response.delete_cookie('carts')
    # 4、响应客户
    return response