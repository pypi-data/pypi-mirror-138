# coding=utf-8
'''
Created on 2021/11/23 11:35
__author__= yanghong
__remark__=
'''
import pymysql
from src.common.log import logger


class MysqlClient:
    db_config = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(MysqlClient, "_instance"):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def connect_db(cls, db_config):
        cls.db_config = db_config
        if hasattr(MysqlClient, 'conn'):  # 多次调用时，先把上一个连接关掉
            cls.cur.close()
            cls.conn.close()
        cls.conn = pymysql.connect(**db_config)
        cls.cur = cls.conn.cursor(cursor=pymysql.cursors.DictCursor)  # 用字典的形式返回查到的数据

    def execute_db(self, sql, dbname=None):
        if dbname and self.db_config['db'] != dbname:  # dbname这个参数传值且与原值不相同时则表示要切换数据库连接
            self.db_config['db'] = dbname
            self.connect_db(self.db_config)
        self.conn.ping()
        if sql.upper().startswith("UPDATE") or sql.upper().startswith("INSERT") or sql.upper().startswith("DELETE"):
            try:
                self.cur.execute(sql)
                self.conn.commit()
            except Exception as e:
                print(f"操作Mysql时出现异常，报错:{e}")
                logger.error(f"操作Mysql时出现异常，报错:{e}")
                self.conn.rollback()
                raise
        else:
            self.cur.execute(sql)
            data = self.cur.fetchall()
            return data


if __name__ == '__main__':
    pass
