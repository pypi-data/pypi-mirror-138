# coding=utf-8
'''
Created on 2022/1/25 13:47
__author__= yanghong
__remark__=
'''
from src.common.http_client_manage import HttpClientManger
class HttpClientBase:
    """
    #keyword内容
    """
    @staticmethod
    def send_request(**kwargs):
        return HttpClientManger().send_http_request(**kwargs)

