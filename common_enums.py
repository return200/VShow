#!/usr/bin/env python
# coding=utf-8
# __project__ = eams
# __author__ = shiyongfei@donews.com
# __date__ = 2018-12-18 
# __time__ = 11:11


class CabinetStatus:
    """
    机柜状态
    """
    USING = 0
    STOPPED = 1
    ABANDONED = 2
    SPARE = 3

    desc = {
        USING: "使用中",
        STOPPED: "停用",
        ABANDONED: "弃用",
        SPARE: "备用"
    }


class HardwareSpecs:
    """
    硬件参数类型
    """
    CPU = 1
    MEMORY = 2
    DISK = 3
    SERVER_MODEL = 4
    OS_VERSION = 5
    SWITCH_MODEL = 6
    MEMORIZER_MODEL = 7
    RAID_LEVEL = 8


class YesNoStatus:
    """
    是否
    """
    YES = 1
    NO = 0

    desc = {
        YES: "是",
        NO: "否"
    }


class UseStatus:
    YES = 1
    NO = 0

    desc = {
        YES: "启用",
        NO: "停用"
    }


class DomainCertType:
    """
    域名证书类型
    """
    WILDCARD = 1
    SINGLE_DOMAIN = 2

    desc = {
        WILDCARD: "通配符",
        SINGLE_DOMAIN: "单域名"
    }


class AssetNoDeviceCode:
    """
    资产编号中的设备类型标识
    """
    SERVER = "F"
    SWITCH = "J"
    MEMORIZER = "C"
    CLOUD = "Y"  # 云服务器，辅助生成云主机的主机编号，非资产编号


class DeviceStatus:
    """
    设备状态
    """
    IDLE = 0
    ONLINE = 1
    DOWN = 2
    STOCK = 3
    SCRAPPED = 4

    desc = {
        IDLE: "空闲",
        ONLINE: "线上",
        DOWN: "故障",
        STOCK: "库存",
        SCRAPPED: "报废"
    }
