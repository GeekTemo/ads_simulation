#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by gongxingfa on 16/3/11

import sys
import string
import urllib
import logging
from Queue import Queue
from requests import Request, Session

from simulation import config

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


def run(redis_host, redis_port, app_id):
    while 1:
        ads_info = ads_request(config.req_info()['method'], config.req_info()['url'], headers=config.headers(),
                               data=config.data(), url_params=config.url_params())
        show_pic_url = ads_info[config.RequestParamsMeta.PIC_URL]
        show_banner_pic_request(show_pic_url)
        ads_link = ads_info[config.RequestParamsMeta.ADS_LINK]
        ads_link_request(ads_link)


if __name__ == '__main__':
    logging.info('Start running.............')
    redis_host = raw_input('Please input the redis host:')
    redis_port = raw_input('Please input the redis port:')
    app_id = raw_input('app id:')
    config.init(redis_host, redis_port, app_id)
    logging.info('Start Success............')
    run(redis_host, redis_port, app_id)
