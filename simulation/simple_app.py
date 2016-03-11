#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by gongxingfa on 16/3/11
import string
import time
import urllib
import json
import requests
from requests import Request, Session
from splinter import Browser


def config():
    data = {
        "sysVer": "9.2.1",
        "height": "736",
        "mac": "02:00:00:00:00:00",
        "productId": "17586",
        "netChannel": "1",
        "width": "414",
        "device": "iPhone",
        "imsi": "46001",
        "idfa": "92C3BA6F-FA7C-4D59-87E1-44B4C8045DDA",
        "jailbroken": "false",
        "versoft": "ios_banner_v1.0",
    }
    method = 'post'
    url = 'http://ads.imopan.com/sec/getTableAd.bin'
    return {'method': method, 'url': url, 'headers': None, 'data': data, 'url_params': None}


def brower():
    return Browser('chrome')


def simulation_ads():
    cf = config()
    b = brower()
    while 1:
        s = Session()
        req = Request(method=string.upper(cf['method']), url=cf['url'], headers=cf['headers'], data=cf['data'],
                      params=cf['url_params'])
        prepped = req.prepare()
        ads_info = json.loads(s.send(prepped).text)['splashAd']
        show_pic_url = ads_info['bannerPicUrl']
        ads_link = urllib.unquote_plus(ads_info['link'])
        requests.get(show_pic_url)
        b.visit(ads_link)
        time.sleep(2)


if __name__ == '__main__':
    simulation_ads()
