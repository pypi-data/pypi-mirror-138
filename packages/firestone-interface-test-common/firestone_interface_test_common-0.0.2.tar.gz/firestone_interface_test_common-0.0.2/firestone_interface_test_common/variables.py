# coding=utf-8
'''
File: variables.py
Created on 2022/2/10 14:41
__author__= yangh
__remark__=
'''


class GlobalVariable:
    """存放具有接口依赖关系的参数"""
    variables_dict = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(GlobalVariable, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance
