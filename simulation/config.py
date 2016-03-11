#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by gongxingfa on 16/3/11
import time
from threading import Thread
from redis import StrictRedis
import schedule


class RequestParamsMeta:
    PIC_URL = 'bannerPicUrl'
    ADS_LINK = 'link'


class _RefreshThread(Thread):
    def run(self):
        schedule.every(5).minutes.do(_refresh)
        while 1:
            schedule.run_pending()
            time.sleep(1)


_HEADERS = {}
_PARAMS = {}
_CLICK_PERCENT = 0.5
_PAGE_STAY_TIME = 3


def init(redis_host, redis_port, appid):
    pass


def _refresh():
    pass


def req_info():
    return {"url": "http://ads.imopan.com/sec/getTableAd.bin", "method": "post"}


def headers():
    return None


def data():
    return {'': ''}


def url_params():
    return ''


def click_percent():
    return 0.5


def page_stay_time():
    return 2
