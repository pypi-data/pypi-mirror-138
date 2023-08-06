# coding=utf-8
'''
Created on 2021/11/23 13:23
__author__= yanghong
__remark__=
'''
import os
from ruamel import yaml


class FileDataOperate:
    @staticmethod
    def read_yaml(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                y = yaml.YAML(typ='unsafe', pure=True)
                dict_content = y.load(f.read())
        except Exception as e:
            raise e
        return dict_content

    @staticmethod
    def resource_path(relative_path):
        # 返回项目根目录
        base_path = os.path.abspath(os.path.dirname(__file__)).split('utils')[0]
        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    pass
