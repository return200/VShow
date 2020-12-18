#!/usr/bin/env python
# coding=utf-8
# __project__ = eams
# __author__ = shiyongfei@donews.com
# __date__ = 2018-12-10 
# __time__ = 14:56
from elasticsearch import helpers


async def es_raw_query(es_conn, index, doc_type, param: dict):
    """
    ES 查询，获得原始响应数据
    :param index:ES 索引
    :param doc_type:ES 文档类型
    :param param: 查询参数
    :return:
    """
    result = es_conn.search(index=index, doc_type=doc_type, body=param)
    print("es_raw_query result:{}".format(result))
    return result


async def es_query(es_conn, index, doc_type, param: dict) -> list:
    """
    ES 查询记录，获得 hits 部分的数据
    :param index:ES 索引
    :param doc_type:ES 文档类型
    :param param:
    :return:
    """
    print("es_query:{} {}".format(index, param))
    tmp_result = await es_raw_query(index, doc_type, param)
    print("es_query result:{}".format(tmp_result))
    result = [x for x in tmp_result.get("hits", {}).get("hits", [])]
    return result


async def es_aggs(es_conn, index, doc_type, param: dict):
    """
    ES 查询聚合结果，获得 aggregations 部分的数据
    :param index:ES 索引
    :param doc_type:ES 文档类型
    :param param:
    :return:
    """
    tmp_result = await es_raw_query(index, doc_type, param)
    aggs = tmp_result.get("aggregations")
    return aggs


async def es_update_by_id(es_conn, index, doc_type, doc_id, param: dict):
    """
    ES 根据文档 id 更新文档数据
    :param index:ES 索引
    :param doc_type:ES 文档类型
    :param doc_id:
    :param param:
    :return:
    """
    print("es_update:{} {} {}".format(index, doc_type, param))
    update_param = {
        "doc": param
    }
    r = es_conn.update(index=index, doc_type=doc_type, id=doc_id, body=update_param)
    print("es_update result:{}".format(r))
    return r


async def es_update_by_query(es_conn, index, doc_type, body: dict):
    """
    ES 根据查询条件更新文档数据，若有冲突则继续
    :param index:ES 索引
    :param doc_type:ES 文档类型
    :param body:
    :return:
    """
    es_conn.update_by_query(index=index, doc_type=doc_type, body=body, conflicts="proceed")


async def es_delete_by_id(es_conn, index, doc_type, doc_id):
    """
    ES 根据文档 id 删除文档
    :param index:ES 索引
    :param doc_type:ES 文档类型
    :param doc_id:
    :return:
    """
    print("es_delete:{} {} {}".format(index, doc_type, doc_id))
    r = es_conn.delete(index=index, doc_type=doc_type, id=doc_id)
    print("es_delete result:{}".format(r))
    return r


async def es_delete_by_query(es_conn, index, doc_type, body: dict):
    """
    ES 根据查询条件删除文档数据，若有冲突则继续
    :param index:ES 索引
    :param doc_type:ES 文档类型
    :param body:
    :return:
    """
    print("es_delete_by_query:{} {} {}".format(index, doc_type, body))
    r = es_conn.delete_by_query(index=index, doc_type=doc_type, body=body, conflicts="proceed")
    print("es_delete_by_query result:{}".format(r))
    return r


async def es_bulk_insert(es_conn, index, doc_type, data):
    """
    批量插入数据
    :param index:ES 索引
    :param doc_type:ES 文档类型
    :param data:要插入的数据，dict 或 list
    :return:
    """
    res = None
    actions = []
    data = data if isinstance(data, list) else [data]
    if data:
        for d in data:
            action = {
                "_index": index,
                "_type": doc_type,
                "_source": d
            }
            actions.append(action)
        res = helpers.bulk(es_conn, actions)
    return res
