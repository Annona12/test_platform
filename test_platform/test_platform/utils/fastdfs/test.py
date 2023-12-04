# -*- coding: utf-8 -*-
# 开发者:Annona
# 开发时间:2023/12/3 16:05
from fdfs_client.client import Fdfs_client

# 1、创建FastDFS客户端实例
client = Fdfs_client('client.conf')

# 2、调用FastDFS客户端上传文件方法
ret = client.upload_by_filename('E:\\python\\test_platform\\test_platform\\image.jpg')
print(ret)