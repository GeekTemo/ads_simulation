#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by gongxingfa on 16/3/11

import sys
import string
import urllib
import logging
import json
import random
import time
from multiprocessing import Process, Queue, current_process
from requests import Request, Session
from splinter import Browser
import requests

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='app.log',
                    filemode='a')

ads_tasks = Queue(1024)


class AdsMeta:
    ClickPercent = 'click_percent'
    PageStayTime = 'page_stay_time'
    Method = 'method'
    URL = 'url'
    ShowPicUrl = 'bannerPicUrl'
    Headers = 'headers'
    Data = 'data'
    Params = 'url_params'
    AdsLink = 'link'
    Modle = "modle"
    Idfa = 'idfa'
    AppId = "appId"
    ProductId = "productId"
    SysVer = 'sysVer'
    Versoft = 'versoft'
    S = 's'


class AdsTaskProducer(Process):
    def __init__(self, config):
        Process.__init__(self)
        self.config = config

    def run(self):
        modle = self.config[AdsMeta.Modle]
        if modle == 'stand_alone':
            reqs = self.config['requests']
            reqs_count = len(reqs)
            i = 0
            while 1:
                ads_task = reqs[i % reqs_count]
                ads_tasks.put(ads_task)
                i += 1
                time.sleep(2)


class AdsSimulator(Process):
    Nums = 1000

    def __init__(self, config):
        Process.__init__(self)
        self.config = config
        self.nums = [0 for i in range(AdsSimulator.Nums)]
        for i in range(int(AdsSimulator.Nums * self.config[AdsMeta.ClickPercent])):
            self.nums[random.randint(0, AdsSimulator.Nums - 1)] = 1
        self.browser = Browser('chrome')

    def _show_pic(self, url):
        self.browser.visit(url)

    @staticmethod
    def _url_encode(params):
        raw = ''
        for key, value in params.items():
            raw += '&' + key + '=' + value
        return raw

    def banner_click(self, ads_info):
        # parms = 'idfa=92C3BA6F-FA7C-4D59-87E1-44B4C8045DDA&appId=101&type=002&productId=17586&sysVer=9.2.1&versoft=ios_banner_v1.0&link=http%3A%2F%2Fitunes.apple.com%2Fcn%2Fapp%2Fid388089858%3Fmt%3D8&s=56beb5f0e3d7274551b97c8f3ea9dfe3'

        params = {AdsMeta.Idfa: ads_info[AdsMeta.Idfa], AdsMeta.AppId: ads_info['id'],
                  'type': 002, 'productId': '17586', 'sysVer': '9.2.1', 'versoft': 'ios_banner_v1.0',
                  'link': urllib.unquote(ads_info[AdsMeta.AdsLink]), 's': '56beb5f0e3d7274551b97c8f3ea9dfe3'}
        url = 'http://ads.imopan.com/sec/bannerClick.bin?'
        url += AdsSimulator._url_encode(params)[1:]
        print 'Click url...', url
        self.browser.visit(url)

    def ads_redirect(self, url):
        url = urllib.unquote(url)
        self.browser.visit(url)

    def _if_ads_click(self):
        return random.choice(self.nums)

    @staticmethod
    def _ads_request(method, url, headers=None, data=None, url_params=None):
        s = Session()
        req = Request(string.upper(method), url, headers=headers, data=data, params=url_params)
        prepped = req.prepare()
        rsp = s.send(prepped)
        return rsp.text

    def run(self):
        logging.warn('Start running ads simulation process: %s' % str(current_process()))
        while 1:
            ads_task = ads_tasks.get()
            try:
                task_info = json.loads(
                    self._ads_request(ads_task[AdsMeta.Method], ads_task[AdsMeta.URL], data=ads_task[AdsMeta.Data]))[
                    'splashAd']
                self._show_pic(task_info[AdsMeta.ShowPicUrl])
                if self._if_ads_click():
                    self.banner_click(task_info)
                    # self.ads_redirect(task_info[AdsMeta.AdsLink])
                    time.sleep(self.config[AdsMeta.PageStayTime])
            except Exception, e:
                logging.error('Ads url:' + ads_task[AdsMeta.URL] + ' request error..')


def run_ads_simulation(cf):
    ads_task_producer = AdsTaskProducer(cf)
    ads_simulator = AdsSimulator(
        config={AdsMeta.ClickPercent: cf[AdsMeta.ClickPercent], AdsMeta.PageStayTime: cf[AdsMeta.PageStayTime]})
    ads_task_producer.start()
    ads_simulator.start()


if __name__ == '__main__':
    # if len(sys.argv) <= 1:
    #     logging.error('Useage "python ads_simulation config.json"')
    #     sys.exit(1)
    logging.warn('Start running ads_simulation.......')
    # cf = json.load(open(sys.argv[1], 'r'))
    cf = json.load(open('config_template.json', 'r'))
    run_ads_simulation(cf)
