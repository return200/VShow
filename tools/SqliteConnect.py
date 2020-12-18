#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/23 6:43 PM
# @Author  : xixi
# @File    : pub_sqlite.py
#import sqlite3 as sqlite
import sqlite

class SqliteConnect:
    def __init__(self,address):
        self.conn = sqlite.connect(address)
        self.cursor =  self.conn.cursor()

    def insert(self,sql):
        self.cursor.execute(sql)
        self.conn.commit()
        # self.conn.close()
    def getresult(self,sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        # self.close()
        return result
    def close(self):
        self.conn.close()
