# -*- coding: utf-8 -*-
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import logging

logger = logging.getLogger(__name__)


class DBUtil(object):
    __base_class = None

    def __init__(self, db_conf, encoding='utf-8', echo=False):
        self._engine = create_engine(db_conf, encoding=encoding, echo=echo)
        session_class = sessionmaker(self._engine)
        self._session = session_class()

    def _table_query(self, table_name):
        """ 避免重复加载，同时只是用execute时，不加载以下内容 """
        if self.__base_class is None:
            self.__base_class = automap_base()
            self.__base_class.prepare(self._engine, reflect=True)
        if hasattr(self.__base_class.classes, table_name):
            table = getattr(self.__base_class.classes, table_name)
            return self._session.query(table)
        else:
            raise KeyError(f"未搜寻到表: {table_name}")

    def execute_sql(self, sql_str, **ft):
        """
        执行sql语句，区分查询跟修改操作
        cursor支持fetchall(),fetchone(),fetchmany(),rowcount
        """
        sql_str = sql_str.format(**ft).strip().replace("\n", "").replace("\t", "")
        logger.info(f"装载SQL语句：{sql_str}")
        if sql_str.startswith("select"):
            cursor = self._engine.execute(sql_str)
            logger.info(f"引擎已执行SQL语句：{sql_str}")
            return cursor
        try:
            affect_row = self._engine.execute(sql_str).rowcount
            self._session.commit()
            logger.info(f"引擎已执行语句: {sql_str}")
            return affect_row
        except Exception as e:
            logger.error(f"引擎故障, 未执行SQL语句：{sql_str}")
            self._session.rollback()
            self.close()
            raise e

    def execute_many_sql(self, many_sql, separator=";", **ft):
        """ 执行多条sql, sql语句之间使用；号分割，方便执行多条修改语句 """
        sql_list = many_sql.format(**ft).strip().replace("\n", "").replace("\t", "").split(separator)
        sql_list = [sql for sql in sql_list if sql.strip() != ""]
        for sql_str in sql_list:
            self.execute_sql(sql_str)

    def delete(self, table_name, ft=None):
        """ 表名 + dict(key=word), 根据ft条件删除数据 """
        ft = {} if ft is None else ft
        delete_row = self._table_query(table_name).filter_by(**ft).delete()
        self._session.commit()
        logger.info(f'清除{delete_row}目标-{table_name}-线索:{ft}')
        return delete_row

    def first(self, table_name, ft=None):
        """ 一行数据 """
        ft = {} if ft is None else ft
        first_row = self._table_query(table_name).filter_by(**ft).first()
        return first_row

    def all(self, table_name, ft=None):
        """ 所有数据 """
        ft = {} if ft is None else ft
        all_row = self._table_query(table_name).filter_by(**ft).all()
        return all_row

    def count(self, table_name, ft=None):
        """ 行数 """
        ft = {} if ft is None else ft
        rowcount = self._table_query(table_name).filter_by(**ft).count()
        return rowcount

    def close(self):
        self._session.close()
        logger.info("会话终结...待续.")
