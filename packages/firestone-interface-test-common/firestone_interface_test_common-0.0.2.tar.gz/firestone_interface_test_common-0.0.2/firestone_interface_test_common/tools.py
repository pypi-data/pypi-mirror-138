# coding=utf-8
'''
Created on 2022/1/25 14:02
__author__= yanghong
__remark__=
'''
import os
import allure
from src.common.valid import AssertPub
from src.common.log import logger
from dingtalkchatbot.chatbot import DingtalkChatbot


def get_project_root_path(path):
    """项目根目录+path"""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), path)


def realize_code(realize_obj, case_data):
    keyword = case_data.get('keyword')
    allure.dynamic.feature(case_data.get("case_feature"))
    allure.dynamic.story(case_data.get("case_story"))
    allure.dynamic.title(case_data.get("case_title"))
    allure.dynamic.description(case_data.get("case_description"))
    realize_obj = realize_obj()
    if not hasattr(realize_obj, keyword):
        raise KeyError(f"{realize_obj}对象中暂无{keyword}方法，请检查！")
    realize_func = getattr(realize_obj, keyword)
    result = realize_func(case_data)
    expect_datas = case_data.get("validate").get("response")
    logger.info("==================================<<  Validate Result Detail  >>==================================")
    for valid_data in expect_datas:
        for valid_type, expect_value in valid_data.items():
            getattr(AssertPub, valid_type)(api_result=result, expect_jsonpath=expect_value[0],
                                           expect_value=expect_value[1])


def send_dd(project_name, message, webhook):
    """
    将结果发送至钉钉
    """
    try:
        ding = DingtalkChatbot(webhook)
        ding.send_text(msg="{}\n {}".format(project_name, message), is_at_all=True)
    except Exception as e:
        raise e


def produce_ids(data):
    """
    制造ids
    :return: list[]
    """
    return [i.get("case_feature") + i.get("case_story") + i.get("case_title") for i in data]


if __name__ == '__main__':
    pass
