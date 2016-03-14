#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by gongxingfa on 16/3/14



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

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='app.log',
                    filemode='a')

ads_tasks = Queue(1024)


class AdsConstant:
    TableAdsUrl = 'http://ads.imopan.com/sec/getTableAd.bin'
    BannerAdsUrl = 'http://ads.imopan.com/sec/getBannerAd.bin'
    TableClickUrl = 'http://ads.imopan.com/sec/tableClick.bin'
    BannerClickUrl = 'http://ads.imopan.com/sec/bannerClick.bin'


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


class AdsSimulator(object):
    Nums = 1000

    def __init__(self, config):
        # Process.__init__(self)
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
            raw += '&' + key + '=' + str(value)
        return raw

    def ads_click(self, url, ads_info):
        ads_type = 001 if url == AdsConstant.TableClickUrl else 002
        params = {'idfa': ads_info[AdsMeta.Idfa], 'appId': ads_info['id'],
                  'type': ads_type, 'productId': ads_info[AdsMeta.ProductId], 'sysVer': '9.2.1',
                  'versoft': 'ios_banner_v1.0',
                  'link': urllib.unquote(ads_info[AdsMeta.AdsLink]), 's': '56beb5f0e3d7274551b97c8f3ea9dfe3'}
        url += '?' + AdsSimulator._url_encode(params)[1:]
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
                task_info[AdsMeta.ProductId] = ads_task[AdsMeta.Data][AdsMeta.ProductId]
                self._show_pic(task_info[AdsMeta.ShowPicUrl])
                if self._if_ads_click():
                    click_url = AdsConstant.TableClickUrl if ads_task[
                                                                 AdsMeta.URL] == AdsConstant.TableAdsUrl else AdsConstant.BannerClickUrl
                    self.ads_click(click_url, task_info)
                    time.sleep(self.config[AdsMeta.PageStayTime])
            except Exception, e:
                logging.error('Ads url:' + ads_task[AdsMeta.URL] + ' request error..')


def run_ads_simulation(cf):
    ads_task_producer = AdsTaskProducer(cf)
    ads_simulator = AdsSimulator(
        config={AdsMeta.ClickPercent: cf[AdsMeta.ClickPercent], AdsMeta.PageStayTime: cf[AdsMeta.PageStayTime]})
    ads_task_producer.start()
    ads_simulator.run()


if __name__ == '__main__':
    # if len(sys.argv) <= 1:
    #     logging.error('Useage "python ads_simulation config.json"')
    #     sys.exit(1)
    logging.warn('Start running ads_simulation.......')
    # cf = json.load(open(sys.argv[1], 'r'))
    cf = json.load(open('config_template.json', 'r'))
    run_ads_simulation(cf)
