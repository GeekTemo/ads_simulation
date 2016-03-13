#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by gongxingfa on 16/3/11

import sys
import string
import urllib
import logging
import json
import random
from multiprocessing import Process, Queue, current_process
from collections import defaultdict
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
    ClickPercent = 'click_prtcent'
    PageStayTime = 'page_stay_time'
    Method = 'method'
    URL = 'url'
    ShowPicUrl = 'banner'
    Headers = 'headers'
    Data = 'data'
    Params = 'url_params'
    AdsLink = 'link'


class AdsTaskProducer(Process):
    def run(self):
        ads_task = defaultdict(lambda: None)
        while 1:
            ads_tasks.put(ads_task)


class AdsSimulator(Process):
    Nums = 1000

    def __init__(self, config):
        Process.__init__(self)
        self.config = config
        self.nums = [0 for i in range(AdsSimulator.Nums)]
        for i in range(AdsSimulator.Nums):
            self.nums[random.choice(0, AdsSimulator.Nums - 1)] = 1
        self.browser = Browser()

    def _init_simulation(self, config):
        logging.warn('init simulation......')

    def _show_pic(self, url):
        requests.get(url)

    def ads_redirect(self, url):
        url = urllib.unquote(url)
        pass

    def _if_ads_click(self):
        return random.choice(self.nums)

    def _ads_request(self, method, url, headers=None, data=None, url_params=None):
        s = Session()
        req = Request(string.upper(method), url, headers=headers, data=data, params=url_params)
        prepped = req.prepare()
        rsp = s.send(prepped)
        return rsp.text

    def run(self):
        logging.warn('Start running ads simulation process: %s' % str(current_process()))
        while 1:
            ads_task = ads_tasks.get()
            task_info = self._ads_request(ads_task[AdsMeta.Method], ads_task[AdsMeta.URL])
            self._show_pic(ads_task[AdsMeta.ShowPicUrl])
            if self._if_ads_click():
                self.ads_redirect(task_info[AdsMeta.AdsLink])


def run_ads_simulation(cf):
    ads_task_producer = AdsTaskProducer()
    ads_simulator = AdsSimulator(config={AdsMeta.ClickPercent: 0.5, AdsMeta.PageStayTime: 3})
    ads_task_producer.start()
    ads_simulator.start()


if __name__ == '__main__':
    logging.warn('Start running ads_simulation.......')
    cf = json.load(open(sys.argv[1], 'r'))
    run_ads_simulation(cf)
