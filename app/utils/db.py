# -*- coding: UTF-8 -*-
import pymysql


class Database(object):
    def __init__(self):
        self.host = 'cdb-76uuco6h.gz.tencentcdb.com'
        self.db = 'gaokao'
        self.user = 'dominique'
        self.pwd = 'Birdy123'
        self.port = 10132
        self._conn = self.connect()
        self._cursor = self._conn.cursor()

    def connect(self):
        print('连接成功')
        return pymysql.connect(
            database=self.db,
            user=self.user,
            password=self.pwd,
            host=self.host,
            port=self.port)

    def close(self):
        self._cursor.close()
        self._conn.close()

    '''
            sql ="SELECT * FROM student where id = %s;"
            params = (1,)
            options: {
                sql: str,
                params: params
                type: str, // fetch type
                number: number
            }
    '''

    def select(self, options, params):
        try:
            fetch_type = options['type']
            sql = options['sql']
            if params:
                self._cursor.execute(sql, params)
            else:
                self._cursor.execute(sql)
            rows = self._cursor.fetchall()
            self._conn.commit()
            return rows
        except Exception as e:
            print(e)
            self._conn.rollback()


    '''
        :param: dict, ex: {"name":"123", "num": 123}
        sql ="""INSERT INTO student (num, name) VALUES (%(num)s, %(name)s)"""
    '''

    def insert(self, sql, params):
        try:
            self._cursor.execute(sql, params)
            print("insert successfully")
            self._conn.commit()
        except Exception as e:
            print(e)

    '''
        :param: 元祖
    '''

    def update(self, sql, params):
        self._cursor.execute(sql, params)
        print("update successfully")
        self._conn.commit()

    def delete(self, sql, params):
        self._cursor.execute(sql, params)
        print("delete successfully")
        self._conn.commit()

    def __del__(self):
        print("最后一步，关闭数据库")
        self.close()