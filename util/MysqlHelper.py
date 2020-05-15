# -*- coding: utf-8 -*-
import pymysql


class MysqlHelper(object):
    conn = None

    def __init__(self, host, username, password, db, charset='utf8', port=3306):
        self.cursor = self.conn.cursor()
        self.host = host
        self.username = username
        self.password = password
        self.db = db
        self.charset = charset
        self.port = port

    def connect(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.username, password=self.password,
                                    db=self.db,
                                    charset=self.charset)

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_one(self, sql, params=()):
        result = None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print(e)
        return result

    def get_all(self, sql, params=()):
        list_data = ()
        try:
            self.connect()
            self.cursor.execute(sql, params)
            list_data = self.cursor.fetchall()
            self.close()
        except Exception as e:
            print(e)
        return list_data

    def insert(self, sql, params=()):
        return self.__edit(sql, params)

    def update(self, sql, params=()):
        return self.__edit(sql, params)

    def delete(self, sql, params=()):
        return self.__edit(sql, params)

    def __edit(self, sql, params):
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql, params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)
        return count
