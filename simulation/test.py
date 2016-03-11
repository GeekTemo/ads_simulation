#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by gongxingfa on 16/3/11


from simulation.app import ads_request


def test_ads_request():
    url = "http://ads.imopan.com/sec/getTableAd.bin"
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
    rsp = ads_request('post', url=url, data=data)
    import json
    rd = json.loads(rsp)
    print type(rd)

test_ads_request()
