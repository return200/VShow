#!/usr/bin/env python
# coding=utf-8
# __project__ = eams
# __author__ = shiyongfei@infinities.com.cn
# __date__ = 2019-06-04 
# __time__ = 15:14
import copy
from urllib.parse import quote

import pandas as pd
import xlwt
from functools import reduce
from io import BytesIO
from sanic import response

from lib.pub_time import now_time_str


class ExcelWriter:
    def __init__(self):
        self.workbook = xlwt.Workbook(encoding='utf8')
        self.sheets = []

        self._header_height = 1

        self._header_style = xlwt.XFStyle()

        al = xlwt.Alignment()
        al.horz = 0x02  # 水平居中
        al.vert = 0x01  # 垂直居中
        self._header_style.alignment = al

        font = xlwt.Font()
        font.bold = True  # 加粗
        font.height = 0x00d0  # 字体高度
        font.name = u"微软雅黑"
        self._header_style.font = font

    def add_sheet(self, sheet_name, header: list, data: list):
        """
        添加 sheet
        :param sheet_name: sheet 名称
        :param header: 表格头
        :param data: 数据,需为 [{"title":"MyData"}] 形式
        :return:
        """
        sheet = {
            "name": sheet_name,
            "header": header,
            "data": data,
        }
        self.sheets.append(sheet)

    def _write_header(self, sheet, header):
        tmp_header = copy.deepcopy(header)

        for h_index, h in enumerate(tmp_header):
            last_max_index = tmp_header[h_index - 1]["range"][-1] if h_index > 0 else -1
            h["range"] = (last_max_index + 1, last_max_index + 1)

        for h in tmp_header:
            left_col, right_row = h.get("range")

            keys = [x for x in h.keys() if x not in ("child", "range")]
            name = h.get(keys[0])
            sheet.write_merge(0, 0, left_col, right_row, name, style=self._header_style)

    @staticmethod
    def _get_bottom_headers(header):
        bottom_headers = [list(x.keys())[0] for x in header]
        return bottom_headers

    def _write_content(self, sheet, header, content):
        headers = self._get_bottom_headers(header)
        data = [[x.get(y) for y in headers] for x in content]
        for col_index, row_data in enumerate(data):
            for row_index, col_data in enumerate(row_data):
                sheet.write(col_index + self._header_height, row_index, col_data)

    def _write(self):
        for sht in self.sheets:
            sht_name = sht.get("name")
            sht_header = sht.get("header")
            sht_content = sht.get("data")

            sheet = self.workbook.add_sheet(sht_name)

            self._write_header(sheet, sht_header)
            self._write_content(sheet, sht_header, sht_content)

    def save_as_local_file(self, file_name, file_extension=".xls"):
        """
        保存为本地文件
        :param file_name:文件名
        :param file_extension: 文件扩展名
        :return:
        """
        self._write()
        file_name = file_name + file_extension
        self.workbook.save(file_name)

    def save_as_net_file(self, file_name, file_extension="xls"):
        """
        保存为网络文件
        :param file_name: 文件名,不含文件类型后缀
        :param file_extension: 文件扩展名
        :return:
        """
        self._write()
        stream = BytesIO()
        self.workbook.save(stream)

        headers = {
            "Pragma": 'no-cache',
            "Content-Type": "application/vnd.ms-excel",
            "Content-Disposition": f"attachment;filename={file_name}.{file_extension}"
        }
        return response.raw(stream.getvalue(), headers=headers)


def export_excel(data: list, header: list, filename: str = None):
    """
    导出excel数据
    :param data:
    :param header:
    :param filename:
    :return:
    """
    buf = BytesIO()
    data = data or [{list(x.keys())[0]: ""} for x in header]
    pd_data = pd.DataFrame(data)

    def _update(x, y):
        x.update(y)
        return x

    rename_columns = reduce(_update, header)
    columns = rename_columns.values()
    pd_data.rename(columns=rename_columns, inplace=True)
    pd_data.to_excel(buf, encoding="utf_8_sig", index=False, columns=columns)
    date_str = now_time_str("%Y%m%d%H%M%S")
    if not filename:
        filename = date_str
    else:
        filename += date_str

    filename = quote(filename)
    headers = {
        "Pragma": 'no-cache',
        "Content-Type": "application/vnd.ms-excel",
        "Content-Disposition": f"attachment;filename={filename}.xls"
    }
    res = response.raw(buf.getvalue(), headers=headers)
    return res


def export_multi_sheet_excel(data: list, filename: str = None):
    """
    导出有多个 sheet 的 Excel
    :param data:
    :param filename:
    :return:
    """
    writer = ExcelWriter()
    for d in data:
        sheet_name = d.get("sheet_name")
        header = d.get("header")
        data = d.get("data")

        writer.add_sheet(sheet_name=sheet_name, header=header, data=data)

    date_str = now_time_str("%Y%m%d%H%M%S")
    if not filename:
        filename = date_str
    else:
        filename += date_str
    filename = quote(filename)
    return writer.save_as_net_file(filename)
