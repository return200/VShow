#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import configparser
import logging
import os
import paramiko
import pymysql
from datetime import datetime
from common_enums import YesNoStatus
from config import db_file
from lib.pub_sqlite import SqliteConnect

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', filename='GetDBSize.log')


class DB(object):
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sc = SqliteConnect(db_file)
        self.now_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        # self.dbmap = self.gather_cnf()

    # def gather_cnf(self):
    def get_size_per_db(self):
        """
        :return:
        """
        # 删除本地cnf文件
        for k in os.listdir('cnf'):
            if k.endswith('cnf'):
                os.remove(k)

        # 查询db主机列表
        sql = f"""SELECT ipaddress FROM server_list WHERE is_delete={YesNoStatus.NO}"""
        server_list = self.conn.getresult(sql)

        # 读取远程主机的cnf文件并保存到本地，以供configparse解析
        for i in server_list:
            host = i[0][0]
            dest = os.path.join('cnf', f'{host}.my.cnf')
            print(f'Reading {host} my.cnf to {dest}')

            try:
                self.client.connect(hostname=host, port=22, username='root', password='8ql6,yhY')
                stdin, stdout, stderr = self.client.exec_command('cat /etc/my.cnf')
                res = stdout.read() or stderr.read()

                with open(f'{dest}', 'a') as fw:
                    fw.write(res.decode('utf-8'))
            except Exception as e:
                logging.error(f'Connect to {host} Failed!. {str(e)}')
            # finally:
            #     self.client.close()

            # 解析对应的my.cnf
            config = configparser.ConfigParser(allow_no_value=True, strict=False)

            # try:
            #     self.client.connect(hostname=i[0], port=22, username='root', password='8ql6,yhY')
            # except Exception as e:
            #     print(f'Connect to {i[0]} Failed!. {str(e)}')

            config.read(dest)
            sections = config.sections()

            # print(host, sections)

            # 查询server_list表中host对应的id
            sql = f"""SELECT `id` FROM instance_list WHERE t2.ipaddress='{host}'"
                        AND is_delete={YesNoStatus.NO}
                    """
            host_id = self.sc.getresult(sql)

            # 遍历解析my.cnf出来的实例，获取该实例下的所有库名称
            for j in sections:
                if not j.startswith('mysqld33'):
                    continue
                port = config.get(j, 'port')
                path = config.get(j, 'datadir')

                # 将实例写入数据库
                sql = f"""insert into instance_list (host_id, port, datadir, create_time, update_time) 
                            values ({host_id[0][0]}, {port}, '{path}', '{self.now_time}', '{self.now_time}')
                        """
                print(sql)
                self.sc.insert(sql)

                # 查询instance_list表中port对应的id
                sql = f"""SELECT t1.id FROM instance_list AS t1 
                            INNER JOIN server_list AS t2 ON t1.host_id=t2.id 
                            WHERE t2.ipaddress='{host}' AND port={port} 
                            AND t1.create_time=(select max(create_time) from instance_list)
                        """
                port_id = self.sc.getresult(sql)

                # 查询某个实例下所有库名称，是一个list
                dblist = self.get_db_name(host, port)
                if len(dblist) == 0:
                    logging.warning(f'{host}:{port} has no avaliable database')
                    continue

                # 计算每个数据库目录的大小
                for k in dblist:
                    # print(os.path.join(path, k))
                    db_dir = os.path.join(path, k)

                    stdin, stdout, stderr = self.client.exec_command("du -s %s |awk '{print $1}'" % db_dir)
                    res = stdout.read().strip() or stderr.read().strip()

                    sql = f"""INSERT INTO db_list (host_id, port_id, db_name, db_size, create_time, update_time) 
                            VALUES ({host_id[0][0]}, {port_id[0][0]}, '{k}', {res.decode('utf-8')}, '{self.now_time}', '{self.now_time}')
                            """
                    print(sql)
                    self.sc.insert(sql)

                    # disk_usage = f"{host}\t{port}\t{db_dir}\t{res.decode('utf-8')}"
                    # print(disk_usage)
                    # self.save_file(disk_usage)
        else:
            self.client.close()

    @staticmethod
    def get_db_name(host: str, port: int) -> list:
        res = []

        try:
            conn = pymysql.connect(host=str(host), port=int(port), user='root', passwd='9002nx624')
        except Exception as e:
            conn = None
            logging.error(f'Connect to {host}:{port} failed!. {str(e)}')

        if conn:
            cursor = conn.cursor()
            cursor.execute('show databases')
            databases = cursor.fetchall()
            for i in databases:
                db_name = i[0]
                if db_name == 'test' or db_name == 'mysql' or db_name.endswith('schema'):
                    continue
                else:
                    res.append(db_name)

            conn.close()
        # print('*'*20,host,port,res)

        return res


if __name__ == '__main__':
    pass
