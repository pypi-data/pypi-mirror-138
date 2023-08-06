# coding=utf-8
'''
Created on 2021/11/23 10:49
__author__= yanghong
__remark__=
'''
import requests
from src.common.log import logger
import json
import time
from functools import wraps


def wrapper_request_log(func):
    """请求详情记录"""

    @wraps(func)
    def collect_request_detail(*args, **kwargs):
        start_time = time.time()
        r = func(*args, **kwargs)
        if not isinstance(r, requests.models.Response):
            raise TypeError(f"对象类型有误。预期接收的类型为：{requests.models.Response}，实际类型为:{type(r)}")
        total_time = (time.time() - start_time) * 1000
        total_time = "%.3f" % total_time
        logger.info("==================================<<  Request Detail  >>==================================")
        logger.info(f"URL:   {r.request.url}")
        logger.info(f"Method:   {r.request.method}")
        logger.info(f"Content-Type:   {r.request.headers.get('Content-Type')}")
        logger.info(f"Headers:   {r.request.headers}")
        logger.info(f"Params:   {json.dumps(kwargs.get('params'), ensure_ascii=False)}")
        logger.info(f"data:   {json.dumps(kwargs.get('data'), ensure_ascii=False)}")
        logger.info(f"Json:   {json.dumps(kwargs.get('json'), ensure_ascii=False)}")
        logger.info(f"Time:   {total_time}ms")
        logger.info("==================================<<  Response Detail  >>==================================")
        logger.info(f"Status_code:   {r.status_code}")
        logger.info(f"Headers:   {r.headers}")
        logger.info(f"Content:   {r.content.decode()}")
        logger.info(f"Cookies:   {r.cookies.get_dict()}")
        return r

    return collect_request_detail


class HttpClientManger:
    """
    请求实现类
    """
    http_session = requests.session()
    root_url = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def update_headers(cls, headers: dict):
        cls.http_session.headers.update(headers)

    @classmethod
    @wrapper_request_log
    def send_http_request(cls, path:str, method:str, verify=True, **kwargs):
        if path.startswith('http'): #path是http开头的，不拼接请求根路径，直接那这个path来请求
            request_url = path
        else:
            request_url = cls.root_url + path
        if method.lower() in ['get', 'post', 'put', 'delete']:
            http_result = cls.http_session.request(
                url=request_url,
                method=method.lower(),
                verify=verify,
                **kwargs
            )
        else:
            logger.error(f"请求方法错误,当前的请求方法为：{method},目前只支持get, post, put, delete")
            raise KeyError(f"请求方法错误,当前的请求方法为：{method},目前只支持get, post, put, delete")
        return http_result


if __name__ == '__main__':
    pass
