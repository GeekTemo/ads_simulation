#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by gongxingfa on 16/3/11

import sys
import string
import urllib
import logging
from requests import Request, Session

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='app.log',
                    filemode='a')


def ads_request(method, url, headers=None, data=None, url_params=None):
    s = Session()
    req = Request(string.upper(method), url, headers=headers, data=data, params=url_params)
    prepped = req.prepare()
    rsp = s.send(prepped)
    return rsp.text


def show_banner_pic_request(url):
    pass


def ads_link_request(url):
    pass


def run():
    pass


if __name__ == '__main__':
    pass
