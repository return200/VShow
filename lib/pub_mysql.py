#!/usr/bin/env python
# coding=utf-8
# __project__ = vshow
# __author__ = shiyongfei@donews.com
# __date__ = 2018-12-12 
# __time__ = 10:29

RET_AFFECTED_ROWS = 1
RET_LAST_ID = 2


def _split_list(data_list: list, sub_list_length: int) -> list:
    """
    将一个list，拆分成多个子列表 ，子列表的最大长度为 sub_list_length
    :param data_list:
    :param sub_list_length:
    :return:
    """
    data_length = len(data_list)
    if data_length <= sub_list_length:
        return [data_list]

    result = []
    for i in range(0, data_length, sub_list_length):
        result.append(data_list[i:i + sub_list_length])

    return result


def _clean_value(value):
    if isinstance(value, str):
        value = value.replace("'", "\\'")
    return value


async def simple_query_mysql(mysql_pool, fields, tb_name, condition: dict = None, db_name: str = "vshow", request=None):
    """
    简单查询 MySQL
    :param mysql_pool:
    :param fields:
    :param tb_name:
    :param condition:
    :param db_name:
    :param request:
    :return:
    """
    fields_str = ",".join([f"`{x}`" for x in fields])
    sql = f"SELECT {fields_str} FROM {db_name}.{tb_name} "
    if condition:
        sql += " WHERE 1=1"
        for k, v in condition.items():
            if isinstance(v, list):
                vs = [f"'{str(x)}'" for x in v]
                sql += f" AND {k} IN ({','.join(vs)})"
            else:
                sql += f" AND {k}='{v}'"

    return query_mysql(mysql_pool, sql, request)


async def query_mysql(mysql_pool, sql, request=None) -> list:
    """
    MySQL 查询
    :param mysql_pool: MySQL连接池
    :param sql: 原始查询的SQL语句
    :param request: HTTP 请求对象
    :return:
    """
    # print(sql)
    if request:
        request["sql"].append(sql)

    mysql_conn = mysql_pool.connection()
    with mysql_conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall() or []
    mysql_conn.close()
    return result


async def query_one(mysql_pool, sql, request=None) -> dict:
    """
    MySQL 查询
    :param mysql_pool: MySQL连接池
    :param sql: 原始查询的SQL语句
    :param request: HTTP 请求对象
    :return:
    """
    # print(sql)
    if request:
        request["sql"].append(sql)
    result = await query_mysql(mysql_pool, sql, request)
    result = result[0] if result else {}
    return result


async def raw_insert_mysql(mysql_pool, sql, ret_type=RET_AFFECTED_ROWS, request=None) -> int:
    """
    MySQL 插入数据
    :param mysql_pool: MySQL连接池
    :param sql: 原始插入的SQL语句
    :param ret_type: 返回类型：1，影响的行数；2，最后插入的id
    :param request: HTTP 请求对象
    :return:
    """
    assert ret_type in (RET_AFFECTED_ROWS, RET_LAST_ID), "invalid ret_type, should be 1 or 2"

    if request:
        request["sql"].append(sql)

    mysql_conn = mysql_pool.connection()
    with mysql_conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.rowcount if ret_type == 1 else cursor.lastrowid
    mysql_conn.commit()
    mysql_conn.close()
    return result


async def insert_mysql(pool, tb_name: str, data: dict, update_fields: list = None,
                       ret_type: int = RET_LAST_ID, db_name: str = "vshow", request=None) -> int:
    """
    MySQL 中插入数据
    :param pool: MySQL连接池
    :param tb_name: 表名
    :param data: 要插入的数据
    :param update_fields: 当唯一索引冲突时，要更新的字段
    :param ret_type: 返回类型：1，影响的行数；2，最后插入的id
    :param db_name: 数据库名
    :param request: HTTP 请求对象
    :return:
    """
    data_fields = sorted(data.keys())
    fields = ",".join(f"`{str(x)}`" for x in data_fields)
    values = ",".join(f"'{data[x]}'" for x in data_fields)
    sql = f"INSERT INTO {db_name}.{tb_name} ({fields}) VALUES ({values})"
    if update_fields:
        sql += " ON DUPLICATE KEY UPDATE {}".format(",".join([f"{x}=VALUES({x})" for x in data_fields]))
    ret = await raw_insert_mysql(pool, sql, ret_type, request)
    return ret


async def batch_insert_mysql(mysql_pool, table: str, fields: list, data: list, update_fields: list = None,
                             db: str = "vshow") -> int:
    """
    MySQL 批量插入数据
    :param mysql_pool:数据库连接池
    :param table: 要插入的数据库表
    :param fields: 要插入的字段列表，需有序
    :param data: 要插入的数据，dict 列表
    :param update_fields: 当唯一索引冲突时要更新的字段
    :param db: 要插入的数据库名
    :return:影响的行数
    """
    assert table, "`table` cannot be empty"
    assert fields, "`fields` cannot be empty"
    if not data:
        print("insert empty data!")
        return 0

    field_str = ",".join([f"`{x}`" for x in fields])

    table_name = f"{db}.{table}" if db else table

    result = 0
    split_data = _split_list(data, 2000)
    for sub_data in split_data:

        value_list = []
        for d in sub_data:
            value_list.append(",".join([f"'{_clean_value(d.get(x))}'" for x in fields]))
        value_str = ",".join([f"({x})" for x in value_list])

        insert_sql = f"""INSERT INTO {table_name}({field_str}) VALUES {value_str}"""
        if update_fields:
            update_str = f" ON DUPLICATE KEY UPDATE {','.join([f'{x}=VALUES({x})' for x in update_fields])}"
            insert_sql += update_str

        tmp = await raw_insert_mysql(mysql_pool, insert_sql)
        result += tmp
    return result


async def raw_update_mysql(mysql_pool, sql: str, request=None) -> int:
    """
    MySQL 更新数据
    :param mysql_pool: MySQL连接池
    :param sql: 原始更新的SQL语句
    :param request: HTTP 请求对象
    :return:
    """
    if request:
        request["sql"].append(sql)

    mysql_conn = mysql_pool.connection()
    with mysql_conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.rowcount
    mysql_conn.commit()
    mysql_conn.close()
    return result


async def raw_delete_mysql(mysql_pool, sql: str, request=None) -> int:
    """
    MySQL 删除数据
    :param mysql_pool: MySQL连接池
    :param sql: 原始更新的SQL语句
    :param request: HTTP 请求对象
    :return:
    """
    if request:
        request["sql"].append(sql)

    mysql_conn = mysql_pool.connection()
    with mysql_conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.rowcount
    mysql_conn.commit()
    mysql_conn.close()
    return result


async def update_mysql(pool, tb_name: str, data: dict, condition: dict = None, db_name: str = "vshow",
                       request=None) -> int:
    """
    更新 MySQL
    :param pool: MySQL连接池
    :param db_name: 数据库名
    :param tb_name: 表名
    :param data: 要更新的数据
    :param condition: 更新的条件
    :param request: HTTP 请求对象
    :return:
    """
    values = ",".join([f"`{k}`='{v}'" for k, v in data.items()])
    sql = f"UPDATE {db_name}.{tb_name} SET {values}"
    if condition:
        sql += " WHERE 1=1"
        for k, v in condition.items():
            if isinstance(v, list):
                vs = [f"'{str(x)}'" for x in v]
                sql += f" AND {k} IN ({','.join(vs)})"
            else:
                sql += f" AND {k}='{v}'"

    ret = await raw_update_mysql(pool, sql, request)
    return ret


if __name__ == '__main__':
    # data = lp.run_until_complete(query_mysql(pool, "SELECT * FROM ad_ad_from_mapping"))
    # print(data)
    pass
