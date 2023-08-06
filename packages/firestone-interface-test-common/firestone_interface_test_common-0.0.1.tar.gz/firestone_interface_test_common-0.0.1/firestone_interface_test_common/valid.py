# coding=utf-8
'''
Created on 2021/11/23 16:05
__author__= yanghong
__remark__=
'''

from src.common.log import logger
import jsonpath
import requests


# 有时间再优化下重复代码的问题
class AssertPub:

    @staticmethod
    def get_jsonpath_result_or_http_status_code(api_result, expect_jsonpath):
        if not isinstance(api_result, requests.models.Response):
            raise KeyError(f"api_result的类型必须是requests.models.Response对象。当前的对象类型为{type(api_result)}")
        if str(expect_jsonpath).startswith('$'):
            try:
                jsonpath_result_or_http_status_code = jsonpath.jsonpath(api_result.json(), expect_jsonpath)[0]
            except Exception as e:
                logger.error(f"获取jsonpath结果失败，当前的jsonpath表达式为：{expect_jsonpath}")
                logger.error(e)
                raise
        else:
            jsonpath_result_or_http_status_code = eval(f"api_result.{expect_jsonpath}")
        return jsonpath_result_or_http_status_code

    @staticmethod
    def eq(api_result, expect_jsonpath, expect_value):
        target_value = AssertPub.get_jsonpath_result_or_http_status_code(api_result, expect_jsonpath)
        logger.info(f"进行接口返回值一致性对比，校验方法：校验两值相等")
        try:
            logger.info(f"接口返回的{expect_jsonpath}值为：{target_value}。预期值为：{expect_value}")
            assert target_value == expect_value
        except AssertionError:
            logger.error(f'接口返回的{expect_jsonpath}值为：{target_value}与预期值：{expect_value}不相等！')
            raise AssertionError(f'{target_value}与{expect_value}不相等！，预期应相等！')
        except Exception as e:
            logger.error(e)
            raise

    @staticmethod
    def not_eq(api_result, expect_jsonpath, expect_value):
        target_value = AssertPub.get_jsonpath_result_or_http_status_code(api_result, expect_jsonpath)
        logger.info(f"进行接口返回值一致性对比，校验方法：校验两值不相等")
        try:
            logger.info(f"接口返回的{expect_jsonpath}值为：{target_value}。预期值为：{expect_value}")
            assert target_value != expect_value
        except AssertionError:
            logger.error(f'接口返回的{expect_jsonpath}值为：{target_value}与预期值：{expect_value}相等！')
            raise AssertionError(f'{target_value}与{expect_value}相等！，预期应不相等！')
        except Exception as e:
            logger.error(e)
            raise

    @staticmethod
    def length_not_eq(api_result, expect_jsonpath, expect_value):
        target_value = AssertPub.get_jsonpath_result_or_http_status_code(api_result, expect_jsonpath)
        logger.info(f"进行接口返回值一致性对比，校验方法：校验两值长度不相等")
        try:
            logger.info(f"接口返回的{expect_jsonpath}长度为：{len(target_value)}。预期长度为：{expect_value}")
            assert len(target_value) != expect_value
        except AssertionError:
            logger.error(f'接口返回的{expect_jsonpath}长度为：{len(target_value)}。校验值：{expect_value}，校验两者长度不相等!')
            raise AssertionError(f'{len(target_value)}与{expect_value}相等！，预期应不相等！')
        except Exception as e:
            logger.error(e)
            raise


if __name__ == '__main__':
    pass