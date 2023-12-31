# -*- coding: utf-8 -*-
# 开发者:Annona
# 开发时间:2023/12/4 17:02
from django.core.files.storage import Storage
from django.conf import settings


class FastDFSStorage(Storage):
    """自定义文件存储系统"""

    def __init__(self, fdfs_base_url=None):
        """
        构造方法，可以不带参数，也可以携带参数
        :param base_url: Storage的IP
        """
        self.fdfs_base_url = settings.FDFS_BASE_URL or fdfs_base_url

    def _open(self, name, mode='rb'):
        """
        用于打开文件
        :param name: 要打开的文件的名字
        :param mode: 打开文件方式
        :return: None
        """
        # 打开文件时使用的，此时不需要，而文档告诉说明必须实现，所以pass
        pass

    def _save(self, name, content):
        """
        用于保存文件
        :param name: 要保存的文件名字
        :param content: 要保存的文件的内容
        :return: None
        """
        # 保存文件时使用的，此时不需要，而文档告诉说明必须实现，所以pass
        pass

    def url(self, name):
        """
        返回name所指文件的绝对URL
        :param name: 要读取文件的引用:group1/M00/00/00/wKhnnlxw_gmAcoWmAAEXU5wmjPs35.jpeg
        :return: http://192.168.103.158:8888/group1/M00/00/00/wKhnnlxw_gmAcoWmAAEXU5wmjPs35.jpeg
        """
        return self.fdfs_base_url + name